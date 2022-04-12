# Procedure: 1) Get 38 Month Binance DATA, Get the classification model ready, target variable and matrix, then run many random forrests.

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import re #Using RegEx to filter through the symbols. 

# Binance library.
from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager
from pandas._libs.tslibs.timestamps import Timestamp
from datetime import timedelta, date
from pandas.core.indexes.base import Index
from pandas.core.reshape.merge import merge

# For coinmarketcap parsing
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import time

# Binance API keys
api_key = ''
api_secret = ''
client = Client(api_key, api_secret)

# MySQL database connector, and parameters
# import mysql.connector
# mydb = mysql.connector.connect(host="localhost", user="root", password="root")
# How to execute a query:
# mycursor = mydb.cursor()
# mycursor.execute("the query")

# ------------------- Converting to CSV and examining the PumpMarketCap Data:  --------------
def ReadCSV():
    df = pd.read_json('allPumps.json')
    #Channels to drop
    df = df[df['exchange'] == 'Binance']
    df.to_csv('pumpsBinanceFull.csv')

#Clear issue's around the data surround their misclassification of what a pump is - they last around 0-1 min, and always occur at a round hour, for example 7pm. Thus, their noting of a 6 min pump at 5:46 is incorrect - the data is particlly incomplete.

# ------------------- Data Cleaning the PumpMarketCap Data:  --------------
def Clean():
    df = pd.read_csv('pumpsBinanceFull.csv')
    #Channels to drop
    df = df[df['exchange'] == 'Binance']
    df = df[df['channelLink'] != 'https://t.me/Chatwithexperts']
    df = df[df['channelLink'] != 'https://t.me/cryptoprofitcoach']
    df = df[df['channelLink'] != 'https://t.me/TheCryptoExpress']
    df = df[df['channelLink'] != 'https://t.me/APE_crypto']
    df = df[df['channelLink'] != 'https://t.me/wallstreetbets']
    df = df[df['channelLink'] != 'https://t.me/binancemoonpump']
    df = df[df['channelLink'] != 'https://t.me/cryptosignalcrazy']
    df = df[df['channelLink'] != 'https://t.me/CryptoPumpAnalytics']
    df = df[df['channelLink'] != 'https://t.me/crypto_pump_island']
    df = df[df['channelLink'] != 'https://t.me/CryptoTree07']
    df = df[df['channelLink'] != 'https://t.me/CryptoZ_TRADER']
    df = df[df['channelLink'] != 'https://t.me/bitcoinpumpgroup']
    df = df[df['channelLink'] != 'https://t.me/BinanceWaves']
    df = df[df['channelLink'] != 'https://t.me/cryptoadvisorchannel']
    df = df[df['channelLink'] != 'https://t.me/Binance_FuturesSignal']
    df = df[df['channelLink'] != 'https://t.me/BinanceTurkish']
    df = df[df['channelLink'] != 'https://t.me/OfficialCryptoNinjaCoach']
    df = df[df['channelLink'] != 'https://t.me/BinanceMegaPump1']
    df = df[df['channelLink'] != 'https://t.me/joinchat/AAAAAEohzxzfbyBEquzPew']
    df = df[df['channelLink'] != 'https://t.me/signals_binance_crypto']
    df = df[df['channelLink'] != 'https://t.me/pumpszerorequiem']
    df = df[df['channelLink'] != 'https://t.me/pumpszerorequiem']
    df = df[df['channelLink'] != 'https://t.me/satoshistreetbets']
    df = df[df['channelLink'] != 'https://t.me/SSBtalk']
    df = df[df['channelLink'] != 'https://t.me/joinchat/AAAAAE-ufWSDXHjNy2rQJA']
    df = df[df['channelLink'] != 'https://t.me/Whalesguide']
    df = df[df['channelLink'] != 'https://t.me/ProAnalysisTrader']
    df = df[df['channelLink'] != 'https://t.me/Pumpingstar']
    df = df[df['channelLink'] != 'https://t.me/thebull_crypto']
    df = df[df['channelLink'] != 'https://t.me/po_support_channel']
    df = df[df['channelLink'] != 'https://t.me/BinanceTradingFutures']
    df = df[df['channelLink'] != 'https://t.me/joinchat/AAAAAFKMXCvyYunhH3dh2g']
    df = df[df['channelLink'] != 'https://t.me/tradingcryptocoach']
    df = df[df['channelLink'] != 'https://t.me/cryptofreesignal']
    df = df[df['channelLink'] != 'https://t.me/joinchat/AAAAAETRfXVAYuIieZ7K6g']
    df = df[df['channelLink'] != 'https://t.me/CryptoVIPsignalTA']
    df = df[df['channelLink'] != 'https://t.me/PumpSignalsAllCryptos']
    df = df[df['channelLink'] != 'https://t.me/TechCryptoAnalyst']
    df = df[df['channelLink'] != 'https://t.me/CryptoVIPsignalTA']
    df = df[df['channelLink'] != 'https://t.me/BinanceProfitSignal']
    df = df[df['channelLink'] != 'https://t.me/thebigcryptopumps']
    df = df[df['channelLink'] != 'https://t.me/cryptonewsnshizzle']
    df = df[df['channelLink'] != 'https://t.me/americanwhales']
    df = df[df['channelLink'] != 'https://t.me/BitAssist']
    df = df[df['channelLink'] != 'https://t.me/cryptofox437']
    df = df[df['channelLink'] != 'https://t.me/solidcryptosignal']
    df = df[df['channelLink'] != 'https://t.me/whaleglobal']

    # Data entries to drop
    df = df[df['ourBuyTime'] != '0001-01-01T00:00:00']

    
    df.to_csv('allPumps.csv')


# ---------- PULLING MARKET DATA FROM Binance
def getDataBinance():

    def split_list(alist, wanted_parts=1):  #Splitting the data up so it can be downloading without placing intense workloads on RAM
        length = len(alist)
        return [ alist[i*length // wanted_parts: (i+1)*length // wanted_parts] 
                for i in range(wanted_parts) ]
    
    # ---------- Finding all market pairs from Binance, REGEXing them, and placing them into a list:
    symbols = []
    exchange_info = client.get_exchange_info()
    for s in exchange_info['symbols']:
     pattern = ".*BTC$" #REGEX FOR ENDING WITH BTC (AS VAST MAJORITY OF PUMPS ARE IN BTC)
     if (re.search(pattern, s['symbol'])): 
         symbols.append(s['symbol'])
    symbols = sorted(symbols) #Done for convenience...
    symbolsList = split_list(symbols, wanted_parts=3)
    

    # ---------- GETTING THE DATASET FOR 1 WEEK:
    countParts = 0
    for t in symbolsList:
        dfmain = pd.DataFrame()
        count = 0
        for i in t:
            klines = client.get_historical_klines(""+i+"", Client.KLINE_INTERVAL_15MINUTE, "38 MONTHS ago UTC") # First ever pump on binance was on 06/09/2018 
            df = pd.DataFrame(klines, columns = ['Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close Time', 'Quote asset volume', 'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore'])
            df = df.drop(columns=['High', 'Low', 'Open', 'Open time', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore']) # Dropping unneeded columns
            df = df.rename(columns={"Close": "Close_Price", "Close Time": "Close_Time", "Quote asset volume": "BTC_Volume", "Number of trades": "Trades", 'Volume': 'Asset_Volume'}) # Renaming columns...
            i = i[:-3]  # Removing last 3 characters from the symbol (BTC), in order to get data to match...
            df.insert(0, column='Symbol', value=i)   # Adding symbol name to columns...
            
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
            
            df = df.dropna() #Dropping all rows with NAN's... As 4 days is the max amount of consecutive NAN's, we will lose 4 days at the start of every datapull. SNAPSHOT NEEDS TO BE A MINIMUM OF 96 HOURS(4 DAYS)     
            dfmain = pd.concat([dfmain, df]) #Concatinate
            count = count + 1
            print(dfmain)
            print("%s/%s %s With %s" % (count, len(t), i, t))
        
        countParts = countParts + 1
        dfmain.to_csv('Binance38Months%s.csv' % (countParts))
    
    dfFinal = pd.DataFrame()
    df1 = pd.read_csv('Binance38Months1.csv')
    df2 = pd.read_csv('Binance38Months2.csv')
    df3 = pd.read_csv('Binance38Months3.csv')
    dfFinal = pd.concat([dfFinal, df1, df2, df3])
    dfFinal.to_csv('Binance38MonthsFINAL.csv')


# ---------- PULLING MARKET DATA/SOCIO-ECONOMIC DATA FROM COINMARKETCAP
def getDataCMC():
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
    'start':'3',
    'limit':'5000',
    'convert':'USD'
    }
    headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': '7c011288-0358-43d3-b95b-0e139e738a67',
    }
    session = Session()
    session.headers.update(headers)
    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        dfMarketCap = pd.json_normalize(data['data'])
        print(dfMarketCap)
        dfMarketCap.to_csv('CoinMarketCap.csv')
    except(ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)


# ---------- PULLING MARKET DATA/SOCIO-ECONOMIC DATA FROM COINGECKO
def getDataCG():

    #We require a function that pulls from the api at an interval, as we get rate limited. Max 1 pull every 2 seconds. 
    #Creates the Binance list of symbols
    symbols = []
    exchange_info = client.get_exchange_info()
    for s in exchange_info['symbols']:
     pattern = ".*BTC$" #REGEX FOR ENDING WITH BTC (AS VAST MAJORITY OF PUMPS ARE IN BTC)
     if (re.search(pattern, s['symbol'])): 
         symbols.append(s['symbol'])
    symbols = sorted(symbols) #Done for convenience...
    dfBinanceSymbols = pd.DataFrame({'Symbol':symbols})
    dfBinanceSymbols = dfBinanceSymbols['Symbol'].str[:-3] #Removing the BTC from all the symbols.

    #Creating a monthly date list to iterate through
    sdate = date(2018,5,14)   # start date
    edate = date(2021,11,14)   # end date
    listOfDates = pd.date_range(sdate,edate-timedelta(days=1),freq='M') # end date
    listOfDates = listOfDates.strftime("%d-%m-%Y")
    listOfDates = listOfDates.astype(str)
    print('----- Dates Used ----')
    print(listOfDates)

    #Initiates session. 
    session = Session()

    #Recieving the list of the ID's, and putting them into a dictionary. Then making the dictionary only so 
    url0 = 'https://api.coingecko.com/api/v3/coins/list'
    try:
        response = session.get(url0)
        data0 = json.loads(response.text)
        
        data0 = pd.json_normalize(data0)
        data0['Symbol'] = data0['symbol'].apply(lambda x: x.upper())

        dfDic = pd.merge(dfBinanceSymbols, data0, on=['Symbol'], how='left')
        dfDic = dfDic.drop_duplicates(subset = "Symbol", keep = "last") #For some reason last gives the desired coin (No idea why they structured it like this.)
        dfDic = dfDic.drop(columns=['symbol', 'name'])

        dfDic  = pd.read_csv('CG_Binance_Dic.csv') #The above is cleaned and set to correct values (Took a while so dont delete the file...)

        print('------- Coins Pulled ------')
        print(dfDic)

        dictionary = pd.Series(dfDic.Symbol.values,index=dfDic.id).to_dict()

    except(ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)

    dfFinal = pd.DataFrame()

    for t in listOfDates:
        for i in list(dictionary.keys()):
            time.sleep(15)  #Waiting as to not overload the API
            url = 'https://api.coingecko.com/api/v3/coins/%s/history?date=%s' % (i,t)
            print(url)
            try:
                response = session.get(url)

                try:
                    data = json.loads(response.text)
                except:
                    continue

                #marketcap
                try:
                    dfCGMktCap = pd.json_normalize(data['market_data']['market_cap'])
                    dfCGMktCap = dfCGMktCap['usd']
                    #symbol
                    dfSymbol = pd.json_normalize(data)
                    dfSymbol = dfSymbol['symbol'].str.upper()

                    dfCommunity = pd.json_normalize(data['community_data'])
                    # dfFaceBook = dfCommunity['facebook_likes'] (For some reason none have facebook data...)
                    dfTwitter = dfCommunity['twitter_followers'] # Followers on twitter at time.
                    dfRedditPosts = dfCommunity['reddit_average_posts_48h']  # Average 48hr posts at time.
                    dfRedditComments = dfCommunity['reddit_average_comments_48h']  # Average 48hr comments at time.
                    dfRedditSubs = dfCommunity['reddit_subscribers'] # Subscribers on Reddit at time.
                    dfRedditActiveAccs = dfCommunity['reddit_accounts_active_48h'] #Activity of accounts over 48 hours.

                    dfCommunity = pd.json_normalize(data['public_interest_stats'])
                    dfAlexaRank = dfCommunity['alexa_rank'] #Ranking of internet traffic to the coins website.

                    dfdate = pd.DataFrame(columns=['Date'], index=None) #NEED TO GET THE DATE IN A GOOD CONDITION.
                    dfdate = dfdate.append({'Date': t}, ignore_index = True)

                    dfEnd = pd.concat([dfdate, dfSymbol, dfCGMktCap, dfTwitter, dfRedditPosts, dfRedditComments, dfRedditSubs, dfRedditActiveAccs, dfAlexaRank], axis=1)
                    dfEnd = dfEnd.rename(columns={'usd':'MktCapUSD', 'symbol':'Symbol'})
                    dfFinal = pd.concat([dfFinal,dfEnd], axis=0)
                    print(dfFinal)
                except Exception as e:
                    continue
            except(ConnectionError, Timeout, TooManyRedirects) as e:
                continue
    dfFinal.to_csv('CG.csv') #Remember to replace 'None' with missing values, and you MUST use XGBOOST (Random forrest cant handle NANs)

def mergeAndExportFull():

    dfCMC = pd.read_csv('CoinMarketCap.csv')
    # Dropping/renaming columns we dont need:
    dfCMC = dfCMC.drop(columns=['id', 'name', 'slug', 'date_added', 'tags', 'max_supply', 'circulating_supply', 'total_supply', 'platform', 'cmc_rank', 'last_updated', 'quote.USD.price', 'quote.USD.volume_24h', 'quote.USD.percent_change_1h', 'quote.USD.volume_change_24h', 'quote.USD.percent_change_24h', 'quote.USD.percent_change_7d', 'quote.USD.percent_change_30d', 'quote.USD.percent_change_60d', 'quote.USD.percent_change_90d', 'quote.USD.market_cap_dominance', 'quote.USD.fully_diluted_market_cap', 'quote.USD.last_updated', 'platform.id', 'platform.name', 'platform.symbol', 'platform.slug', 'platform.token_address']) # Dropping unneeded columns
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

    # ---------- CONSTRUCTING TARGET VECTOR FROM PUMPOLYMP DATA
    # read P&D data obtained from PumpOlymp website (premiereship)
    dfPO = pd.read_csv('allPumps.csv')
    dfPO = dfPO[dfPO['exchange'] == 'Binance'] # Dropping all non-binance rows..
    dfPO = dfPO.drop(columns=['exchange', 'channelTitle', 'channelLink', 'max', 'priceBeforePump', 'duration', 'volume', 'ourBuyPrice', 'ourBuyTime', 'ourProfit', 'theoreticalBuyPrice', 'theoreticalBuyTime', 'theoreticalProfit', 'id', 'commonPumpId', 'channelId']) # Dropping unneeded columns
    dfPO = dfPO.rename(columns={"currency": "Symbol", "signalTime": "Close_Time"}) # Renaming columns...
    dfPO['Close_Time'] = pd.to_datetime(dfPO['Close_Time']).dt.tz_convert(None) # converting to date-time format
    dfPO['Close_Time'] = dfPO['Close_Time'].dt.round('15min')   # Rounding to nearest 15 mins
    dfPO = dfPO.sort_values("Close_Time") # Sort columns by market cap.. keeping second(largest market cap of duplicate)
    dfPO = dfPO.drop_duplicates(subset = ["Symbol", "Close_Time"], keep = "last")
    dfPO['Close_Time'] = pd.to_datetime(dfPO['Close_Time']) - timedelta(minutes=15)  # Removing 15 mins (to get the close time that we're at), now removing 1 second (to match close time)
    dfPO['Close_Time'] = pd.to_datetime(dfPO['Close_Time']) - timedelta(milliseconds=1)  # Removing 15 mins (to get the close time that we're at), now removing 1 second (to match close time)
    dfPO = dfPO.sort_values("Symbol")
    dfPO['willPump'] = 1
    dfPO.drop(dfPO.columns[dfPO.columns.str.contains('unnamed',case = False)],axis = 1, inplace = True)
    print('------------ PumpOlymp Data ------')
    print(dfPO)

    # ---------- PULLING Main data, changing UNIX to datetime
    dfmain = pd.read_csv('Binance38MonthsFINAL.csv')
    dfmain.drop(dfmain.columns[dfmain.columns.str.contains('unnamed',case = False)],axis = 1, inplace = True)
    dfmain['Close_Time'] = pd.to_datetime(dfmain['Close_Time'], origin='unix', unit='ms') # Converting Timestamp

    # ---------- Merging MainData with CoinMC data
    dfmain = pd.merge(dfCMC, dfmain, on='Symbol', validate="1:m") #NEEDS RE-EVALUATING, AND MERGING ON DATES TOO! - SAME CLOSE TIMES BUT WITH DIFFERENT MARKET CAPS! LOOK INTO IT.
    print('----------- Imported Binance Data ------')
    print(dfmain)

    # ---------- Merging MainData with PumpOlymp data, and saving it as a CSV (we are then finished)
    dfmain = pd.merge(dfmain, dfPO, on=['Symbol', 'Close_Time'], how='left') # merging to maintain all maindf rows, creating many NAN values for willPump.
    dfmain['willPump'] = dfmain['willPump'].fillna(0) # Replacing these NAN values for 0's, indicating they were not pumped.
    dfmain = dfmain.sort_values(by=['Symbol', 'Close_Time'])
    print(dfmain[dfmain['willPump'] == 1]) # Pumps within the Dataset.
    dfmain.to_csv('RhoBotFull.csv') 


# ---------- Reducing the size of the Full data by randomly deleting non 'will pump' rows - This is a form of manual random undersampling - Go for 0.001% of the values, and work out the ratio. Dont be afraid to do 3/4 files too for safety --------
def reduceSizeAndChunk():
    chunk_size = 3000000
    fraction = 0.9

    data = pd.read_csv('C:\RhoBot\Training_GetData\Data\RhoBotFull.csv', chunksize=chunk_size)
    dfExport = pd.DataFrame()

    for chunk in data:

        chunk.drop(chunk.columns[chunk.columns.str.contains('unnamed',case = False)],axis = 1, inplace = True)
        chunk = chunk.sort_values("Symbol")

        symbols = []
        exchange_info = client.get_exchange_info()

        for s in exchange_info['symbols']:
            pattern = ".*BTC$" #REGEX FOR ENDING WITH BTC (AS VAST MAJORITY OF PUMPS ARE IN BTC)
            if (re.search(pattern, s['symbol'])): 
                symbols.append(s['symbol'])
            symbols = sorted(symbols) #Done for convenience...
            
        for i in symbols:
            i = i[:-3]
            print(i)
            print(chunk[(chunk["willPump"] == 0) & (chunk["Symbol"] == i)])
            chunk = chunk.drop(chunk[(chunk["willPump"] == 0) & (chunk["Symbol"] == i)].sample(frac=fraction).index)  #frac is the percentage to delete.
            print(chunk)

        dfExport = pd.concat([dfExport, chunk], ignore_index=True)      

    dfExport.to_csv("RhoBot%s.csv" % (1-fraction))
reduceSizeAndChunk()



