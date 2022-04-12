# Procedure: 1) Get 38 Month Binance DATA, Get the classification model ready, target variable and matrix, then run many random forrests.

import numpy as np
import pandas as pd
import re #Using RegEx to filter through the symbols. pip install regex

# Binance library.
from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager #pip install python-binance
from pandas._libs.tslibs.timestamps import Timestamp
from datetime import timedelta, date
from pandas.core.indexes.base import Index
from pandas.core.reshape.merge import merge

# For coinmarketcap parsing
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import time
import schedule

# For Threading
import threading
import pickle

# Importing ML libraries
import sklearn
import matplotlib.pyplot as plt
from sklearn import ensemble
import seaborn as sb; sb.set()
import xgboost as xgb
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KernelDensity
from sklearn.svm import SVC
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score, recall_score
from sklearn.metrics import f1_score, roc_auc_score, roc_curve


import mysql.connector
from mysql.connector import errorcode

#MYSQL connection pip install pip install mysql-connector==2.1.7
import mysql.connector
from mysql.connector import errorcode
try:
  cnx = mysql.connector.connect(user='', password='',
                                host='', database='')
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)
else:
  print("You are connected!")

#defining the cursor.
mycursor = cnx.cursor()

# Binance API keys
api_key = ''
api_secret = ''
client = Client(api_key, api_secret)

#

#Defining the dataframe for later.
dfSnapShot = pd.DataFrame()

def snapshot():

    global dfSnapShot

    # ---------- Finding all market pairs from Binance, REGEXing them, and placing them into a list:
    symbols = []
    exchange_info = client.get_exchange_info()
    for s in exchange_info['symbols']:
     pattern = ".*BTC$" #REGEX FOR ENDING WITH BTC (AS VAST MAJORITY OF PUMPS ARE IN BTC)
     if (re.search(pattern, s['symbol'])): 
         symbols.append(s['symbol'])
    symbols = sorted(symbols) #Done for convenience...
    print(len(symbols))
    print(symbols)

    def coinPreviousRow(coin):

        global dfSnapShot

        klines = client.get_historical_klines(""+coin+"", Client.KLINE_INTERVAL_15MINUTE, "193 HOURS ago UTC") # First ever pump on binance was on 06/09/2018 
        df = pd.DataFrame(klines, columns = ['Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close Time', 'Quote asset volume', 'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore'])
        df = df.drop(columns=['High', 'Low', 'Open', 'Open time', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore']) # Dropping unneeded columns
        df = df.rename(columns={"Close": "Close_Price", "Close Time": "Close_Time", "Quote asset volume": "BTC_Volume", "Number of trades": "Trades", 'Volume': 'Asset_Volume'}) # Renaming columns...
        coin = coin[:-3]  # Removing last 3 characters from the symbol (BTC), in order to get data to match...
        df.insert(0, column='Symbol', value=coin)   # Adding symbol name to columns...
        
        df['Close_Price'] = pd.to_numeric(df['Close_Price'], errors='coerce') # Converting numerical columns to numerical datatypes... 
        df['Asset_Volume'] = pd.to_numeric(df['Asset_Volume'], errors='coerce')
        df['BTC_Volume'] = pd.to_numeric(df['BTC_Volume'], errors='coerce')
        
        # INSERTING INTRINSIC FEATURES
        interval = [1, 2, 3, 4, 8, 12, 16, 24, 36, 48, 60, 96, 144, 192, 240, 288, 384] #Features are iterated over 15mins, 30mins, 45mins, 1hr, 2hr, 3hr, 6hrs, 9hrs, 12hrs, 15hrs, 24hrs, 36hrs, 48hrs, 60hrs, 72hrs, 96hrs... 
        for s in interval:
            inhours = s * 0.25
            df['logReturns%sh' % (inhours)] = np.log(df['Close_Price']/df['Close_Price'].shift(s)) #Adding log returns, used log returns as it's additative, and can be used in combination with volatility measures below...
            df['volLogReturns%sh' % (inhours)] = df['logReturns%sh' % (inhours)].rolling(s+1).std() #Creating volatility, note that it's s+1 as log returns is already formed from a rolling (thus 1 s.d is lost) (Volatility is calculated in standard errors)
            
            df['volumeBTCfrom%sh' % (inhours)] = df['BTC_Volume'].rolling(s).sum() #Adding rolling window sum of volume
            df['volVolumeBTCfrom%sh' % (inhours)] = df['volumeBTCfrom%sh' % (inhours)].rolling(s+1).std() #Creating volatility, note that it's s+1 as log returns is already formed from a rolling (thus 1 s.d is lost)
            
            df['volumeASSETfrom%sh' % (inhours)] = df['Asset_Volume'].rolling(s).sum()
            df['volVolumeASSETfrom%sh' % (inhours)] = df['volumeASSETfrom%sh' % (inhours)].rolling(s+1).std() #Creating volatility, note that it's s+1 as log returns is already formed from a rolling (thus 1 s.d is lost)
        
        df = df.dropna() #Dropping all rows with NAN's... As 4 days is the max amount of consecutive NAN's, we will lose 4 days at the start of every datapull. SNAPSHOT NEEDS TO BE A MINIMUM OF 96 HOURS(4 DAYS) * 2 = 9 DAYS 
        print(df)
        df = df.iloc[[2]]
        dfSnapShot = pd.concat([dfSnapShot, df])
        print(dfSnapShot)

    for eachSymbol in symbols:
        time.sleep(0.9) #As to not overload the binance API limit of 1200 calls per min.
        threading.Thread(target=coinPreviousRow,args=(eachSymbol,)).start()
    
    dfSnapShot = dfSnapShot.sort_values('Symbol')
    dfSnapShotTime = dfSnapShot
    print(dfSnapShot)
    time.sleep(10) #Sleeping for 5 seconds to prevent any excess spillover. 
    
    # ---------- RETRIEVING MARKET CAP:
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
    'start':'3',
    'limit':'5000',
    'convert':'USD'
    }
    headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': '',
    }
    session = Session()
    session.headers.update(headers)

    dfCMC = pd.read_csv('CoinMarketCap.csv')
    
    response = session.get(url, params=parameters)
    data = json.loads(response.text)
    print(data)

    try:
      dfCMC = pd.json_normalize(data['data'])
      print('Using new coinmarketcap data.')
      dfCMC.to_csv('CoinMarketCap.csv')
    except KeyError as e:
      print(e)
      print('Using old marketcap data.')

    print(dfCMC)


    # Dropping/renaming columns we dont need:
    dfCMC = dfCMC.drop(columns=['id', 'name', 'slug', 'date_added', 'tags', 'max_supply', 'self_reported_circulating_supply', 'self_reported_market_cap', 'circulating_supply', 'total_supply', 'platform', 'cmc_rank', 'last_updated', 'quote.USD.price', 'quote.USD.volume_24h', 'quote.USD.percent_change_1h', 'quote.USD.volume_change_24h', 'quote.USD.percent_change_24h', 'quote.USD.percent_change_7d', 'quote.USD.percent_change_30d', 'quote.USD.percent_change_60d', 'quote.USD.percent_change_90d', 'quote.USD.market_cap_dominance', 'quote.USD.fully_diluted_market_cap', 'quote.USD.last_updated', 'platform.id', 'platform.name', 'platform.symbol', 'platform.slug', 'platform.token_address']) # Dropping unneeded columns
    dfCMC = dfCMC.rename(columns={"symbol": "Symbol", "quote.USD.market_cap": "MktCapUSD"}) # Renaming columns...
    dfCMC = dfCMC.sort_values("Symbol") # Sort columns...
    dfCMC.drop(dfCMC.columns[dfCMC.columns.str.contains('unnamed',case = False)],axis = 1, inplace = True)
    #Checking Uniqueness
    checkUnique = dfCMC['Symbol'].unique()
    print(len(checkUnique)) # Returns 4644, with 49999 coins returned this means many coins have duplicates, that need deletion.
    dfCMC = dfCMC.sort_values("MktCapUSD") # Sort columns by market cap.. keeping second(largest market cap of duplicate)
    dfCMC = dfCMC.drop_duplicates(subset = "Symbol", keep = "last")
    print('------------ CoinMarketCap Data ------')
    print(dfCMC)

    # ---------- PULLING Main data, changing UNIX to datetime
    dfSnapShot['Close_Time'] = pd.to_datetime(dfSnapShot['Close_Time'], origin='unix', unit='ms') # Converting Timestamp

    # ---------- Merging MainData with CoinMC data
    dfSnapShot = pd.merge(dfCMC, dfSnapShot, on='Symbol', validate="1:m") #NEEDS RE-EVALUATING, AND MERGING ON DATES TOO! - SAME CLOSE TIMES BUT WITH DIFFERENT MARKET CAPS! LOOK INTO IT.
    print(dfSnapShot)

    # ---------- PreProssesing for Prediction:
    dfSnapShot.drop(dfSnapShot.columns[dfSnapShot.columns.str.contains('unnamed',case = False)],axis = 1, inplace = True) #removing unnamed collumn
    print("DFSNAPSHOT OF TIME------")
    print(dfSnapShotTime)
    dfSnapShot = dfSnapShot.drop(columns=['Close_Time'])
    dfSnapShot_Symbol = dfSnapShot['Symbol'] #Keeping the symbol column for after
    dfSnapShot = dfSnapShot.drop(columns=['Symbol']) #Dropped to maintain X with the correct columns 
    print('--------------- PREPROSSESED SNAPSHOT -----------')
    print(dfSnapShot)



    # ---------- Prediction:
    loaded_model = pickle.load(open("RhoBot3.sav", "rb"))

    y_predict_proba = loaded_model.predict_proba(dfSnapShot)

    submission = pd.DataFrame({
     "Symbol":list(dfSnapShot_Symbol), #to list so it can be made a column
     "probabilities":list(y_predict_proba)
     })
    print(submission)

    submission['probabilities'] = submission['probabilities'].str[1] #Retrieving only the probability of a pump
    submission = submission.sort_values('probabilities').tail(4)
    print(submission)

    Stamp = str(dfSnapShotTime.iat[0,3])
    dfSnapShotTime['Close_Time'] = pd.to_datetime(dfSnapShotTime['Close_Time'], origin='unix', unit='ms') # converting to date-time format
    dfSnapShotTime['Close_Time'] = pd.to_datetime(dfSnapShotTime['Close_Time']) + timedelta(minutes=15)  # Removing 15 mins (to get the close time that we're at), now removing 1 second (to match close time)
    dfSnapShotTime['Close_Time'] = pd.to_datetime(dfSnapShotTime['Close_Time']) + timedelta(milliseconds=1)  # Removing 15 mins (to get the close time that we're at), now removing 1 second (to match close time)
    Time_Predicted = str(dfSnapShotTime.iat[0,3])
    print(Time_Predicted)

    One_Name = submission.iat[3,0]
    One_Confidence = int(submission.iat[3,1] * 100)
    print(One_Confidence)

    Two_Name = submission.iat[2,0]
    Two_Confidence = int(submission.iat[2,1] * 100)
    print(Two_Confidence)

    Three_Name = submission.iat[1,0]
    Three_Confidence = int(submission.iat[1,1] * 100)
    print(Three_Confidence)

    Four_Name = submission.iat[0,0]
    Four_Confidence = int(submission.iat[0,1] * 100)
    print(Four_Confidence)

    global mycursor
    global cnx

    print('--------------- POSTING TO DATABASE -----------')
    query = ('INSERT INTO `Predictions` (`Stamp`, `Time`, `Coin_1`, `Confidence_1`, `Coin_2`, `Confidence_2`, `Coin_3`, `Confidence_3`, `Coin_4`, `Confidence_4`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)')
    values = (Stamp, Time_Predicted, One_Name, One_Confidence, Two_Name, Two_Confidence, Three_Name, Three_Confidence, Four_Name, Four_Confidence)
    mycursor.execute(query, values)
    cnx.commit() # making sure the data is commited. 
    print("Commited to the database")

    dfSnapShot = pd.DataFrame() #Reseting snapshot to be empty

def startSnapshot():
    try:
        snapshot()
    except:
        print("an Error occured")
    
#Creating repeating functions as to keep updating the predictions to the database. 
schedule.every(1).hours.at(":00").do(startSnapshot)
schedule.every(1).hours.at(":15").do(startSnapshot)
schedule.every(1).hours.at(":30").do(startSnapshot)
schedule.every(1).hours.at(":45").do(startSnapshot)

snapshot()
while True:
    schedule.run_pending()
    time.sleep(1)





