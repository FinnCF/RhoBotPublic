/*
To implement:
    - A webserver that provides predictions ONLY when 
    - What do they get back after sending the transaction?
*/

const express = require('express');
const mysql = require("mysql2/promise")
var cors = require('cors');
var requestIp = require('request-ip');
const path = require('path');
const http = require('http');
const { verify } = require('crypto');
const ethers = require('ethers')

//Alchemy API key
const arb_KEY = ''

//Connecting to ethers for verification:
const provider = new ethers.providers.AlchemyProvider('arbitrum-rinkeby', arb_KEY)

//Defining the port. 
const port = process.env.PORT || 8080;

//Creating express application:
var app = express();

//Setting the website to be statically used. 
app.use(express.static(path.join(__dirname, 'theme'))); //  "public" off of current is root

//Setting the website to take CORS
app.use(cors()); 
app.use(express.json());

//Initiating MySQL (install mysql2)
const pool = mysql.createPool({
    connectionLimit: 10,
    host: '',
    user: '',
    password: '',
    database: 'RhoBot'
})


/**
 * Checks for whether the hash given in the post request has already been used in a previous prediction.
 * This is to prevent multiple predictions with the same hash. Returns true when the check is positive.
 * @param {string} hash
 * @returns {boolean} 
 */
async function previousPredictionCheck(hash) {

    let data = {}
    //Sending out an sql_request for all predictions. 
    const sql_request = 'SELECT COUNT(hash) AS count FROM Predictions_Log WHERE hash="'+ hash + '";';

    await pool.query(sql_request).then((results) => {
        data = results
    }).catch(function(err){  
    console.log(String(err));
    });

    if(parseFloat(data[0][0].count) == 0) {
        //Returns true when there is no hash in the DB
        return true
    }
    else {
        console.log("Prediction has already been made for this hash.")
        return false
    }
}


/**
 * Checks whether the address and hash given in the post request align. That is, that the hash is from a transaction made by the address.
 * Also checks if the address is valid. Returns true is positive (all is alright)
 * @param {string} address
 * @param {string} hash
 * @returns {boolean}
 */
async function addressAndHashCheck(address, hash) {

    //Pulls out the information relating to the transation
    const hashCheck = await provider.getTransaction(hash)

    //Indexes the address from the hash. 
    const hashCheckAddress = hashCheck.from

    //Checks if the address that was given is valid. Returns true if exists
    const addressCheck = ethers.utils.isAddress(address)

    if (hashCheckAddress.toLowerCase() == address.toLowerCase() && addressCheck == true){
        return true
    }
    else {
        return false
    }
}


app.post('/prediction', async (req, res) => {

    //verifying the address matches with the hash and signature
    const decodedAddress = ethers.utils.verifyMessage(req.body.hash, req.body.signature)

    //Checks if a prediction has already been made with that hash. 
    const previousRequestCheck = await previousPredictionCheck(req.body.hash);

    //Checks if the transcation is from that address, and if the address exists. 
    const addressAndHashCorrect = await addressAndHashCheck(req.body.address, req.body.hash)

    //If address that send post is equal to the signer, and there is no previous transaction, and the address gave the transaction, give the prediction. 
    if(decodedAddress.toLowerCase() == req.body.address.toLowerCase() && previousRequestCheck == true && addressAndHashCorrect == true) {

        console.log("Verified Request made for a /prediction from: " + requestIp.getClientIp(req) + " at " + new Date().getTime())

        //Pulling predictions from the databse and sending it back to the caller
        await pool.query('SELECT * FROM Predictions ORDER BY Stamp DESC LIMIT 1;').then((results) => {
            res.send(results[0])
        }).catch(function(err){  
        console.log(String(err));
        });

        //Inserting the predicitons into the log of the DB. 
        await pool.query('INSERT INTO `Predictions_Log` (`time`, `timestamp`, `ip`, `address`, `hash`, `signature`) VALUES ("'+ new Date() + '", "'+ new Date().getTime() + '", "' + requestIp.getClientIp(req) + '", "' + req.body.address.toLowerCase() + '", "' + req.body.hash + '", "' + req.body.signature + '");').catch(function(err){  
        console.log(String(err));
        });
        
    }
    else {
        console.log('Account was not verified')
        res.send("Account not verified")
    }
})

app.get('/all', async (req, res) => {

    const clientIp = requestIp.getClientIp(req); //getting the ip of the requester.
    console.log("Request made for a /all from: " + clientIp + " at " + new Date().getTime())

    //Making the pool query. 
    await pool.query('SELECT * FROM Predictions LIMIT 1000 OFFSET 4;').then((results) => {
        res.send(results[0])
    }).catch(function(err){  
    console.log(String(err));
    });

    //Logging the pool query.
    await pool.query('INSERT INTO `All_Log` (`time`, `ip`, `request`) VALUES ("'+ new Date().getTime() + '", "' + clientIp + '", "/all")').catch(function(err){  
    console.log(String(err));
    });
})

app.get('/status', async (req, res) => {
    //Pulling an arbitrary datapoint from the DB to check if it works.
    res.send(await pool.query('SELECT * FROM Test').catch(function(err){  
        res.send(err.code);
    }))
})

app.listen(port);
console.log('Listening on port ' + port);

