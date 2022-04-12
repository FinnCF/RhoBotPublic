//Environmental varianbles
const RhoABI = [
  {
    "inputs": [],
    "stateMutability": "nonpayable",
    "type": "constructor"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "internalType": "address",
        "name": "owner",
        "type": "address"
      },
      {
        "indexed": true,
        "internalType": "address",
        "name": "spender",
        "type": "address"
      },
      {
        "indexed": false,
        "internalType": "uint256",
        "name": "value",
        "type": "uint256"
      }
    ],
    "name": "Approval",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": false,
        "internalType": "address",
        "name": "_address",
        "type": "address"
      }
    ],
    "name": "LogPrediction",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "internalType": "address",
        "name": "previousOwner",
        "type": "address"
      },
      {
        "indexed": true,
        "internalType": "address",
        "name": "newOwner",
        "type": "address"
      }
    ],
    "name": "OwnershipTransferred",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "internalType": "address",
        "name": "from",
        "type": "address"
      },
      {
        "indexed": true,
        "internalType": "address",
        "name": "to",
        "type": "address"
      },
      {
        "indexed": false,
        "internalType": "uint256",
        "name": "value",
        "type": "uint256"
      }
    ],
    "name": "Transfer",
    "type": "event"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "owner",
        "type": "address"
      },
      {
        "internalType": "address",
        "name": "spender",
        "type": "address"
      }
    ],
    "name": "allowance",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "",
        "type": "uint256"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "spender",
        "type": "address"
      },
      {
        "internalType": "uint256",
        "name": "amount",
        "type": "uint256"
      }
    ],
    "name": "approve",
    "outputs": [
      {
        "internalType": "bool",
        "name": "",
        "type": "bool"
      }
    ],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "account",
        "type": "address"
      }
    ],
    "name": "balanceOf",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "",
        "type": "uint256"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "account",
        "type": "address"
      },
      {
        "internalType": "uint256",
        "name": "amount",
        "type": "uint256"
      }
    ],
    "name": "burn",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "decimals",
    "outputs": [
      {
        "internalType": "uint8",
        "name": "",
        "type": "uint8"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "spender",
        "type": "address"
      },
      {
        "internalType": "uint256",
        "name": "subtractedValue",
        "type": "uint256"
      }
    ],
    "name": "decreaseAllowance",
    "outputs": [
      {
        "internalType": "bool",
        "name": "",
        "type": "bool"
      }
    ],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "spender",
        "type": "address"
      },
      {
        "internalType": "uint256",
        "name": "addedValue",
        "type": "uint256"
      }
    ],
    "name": "increaseAllowance",
    "outputs": [
      {
        "internalType": "bool",
        "name": "",
        "type": "bool"
      }
    ],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "account",
        "type": "address"
      },
      {
        "internalType": "uint256",
        "name": "amount",
        "type": "uint256"
      }
    ],
    "name": "mint",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "name",
    "outputs": [
      {
        "internalType": "string",
        "name": "",
        "type": "string"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "owner",
    "outputs": [
      {
        "internalType": "address",
        "name": "",
        "type": "address"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "predict",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "renounceOwnership",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "symbol",
    "outputs": [
      {
        "internalType": "string",
        "name": "",
        "type": "string"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "totalSupply",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "",
        "type": "uint256"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "to",
        "type": "address"
      },
      {
        "internalType": "uint256",
        "name": "amount",
        "type": "uint256"
      }
    ],
    "name": "transfer",
    "outputs": [
      {
        "internalType": "bool",
        "name": "",
        "type": "bool"
      }
    ],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "from",
        "type": "address"
      },
      {
        "internalType": "address",
        "name": "to",
        "type": "address"
      },
      {
        "internalType": "uint256",
        "name": "amount",
        "type": "uint256"
      }
    ],
    "name": "transferFrom",
    "outputs": [
      {
        "internalType": "bool",
        "name": "",
        "type": "bool"
      }
    ],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "newOwner",
        "type": "address"
      }
    ],
    "name": "transferOwnership",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  }
]
const RhoAddress = '0xa01A88D21F2C1264F37316d3e101345DB5c3e898';

function setUniswap() {
  //Setting iframe of Uniswap
  uniswap = document.getElementById('uniswap');
  uniswap.innerHTML =  `<iframe src="https://app.uniswap.org/#/swap?theme=dark&inputCurrency=ETH&outputCurrency=${RhoAddress}" scrolling="no" style="border: 0; margin: 0 auto; display: block; border-radius: 12px; max-height: 100%; min-width: -webkit-fill-available; height: 606px;"></iframe>`
}

setUniswap()

//Main accounts variable
let accounts = '';
let balance = 0;
let contract = {};
let provider = {};
let signer = {};


//Viewing if ethereum extension is present on the page
if (typeof window.ethereum !== 'undefined') {
  console.log('MetaMask is installed!');
}


//Connects the ethereum extension to the web3 wallet. 
async function connect() {
  //Making the request for an ethereum wallet
  accounts = await ethereum.request({ method: 'eth_requestAccounts' });

  //Getting the provider
  provider = new ethers.providers.Web3Provider(window.ethereum)

  //Contract 
  contractUnsigned = new ethers.Contract(RhoAddress, RhoABI, provider);

  //Getting the signer (wallet etc)
  signer = provider.getSigner()

  //Changing the contract into a signed version
  contract = contractUnsigned.connect(signer);

  //Setting the Rho balance of the account
  balance = parseInt(await contract.balanceOf(accounts[0]));
}


//Sets the InnerText of the 'connect wallet' button.
async function innerTextButton() {
  let button = document.getElementsByClassName('connectButton')[0];

  if (accounts == undefined) {
    button.innerText = "Connect Wallet";
  }
  else {
    button.innerText = balance + " RHO | " + accounts[0].slice(0,4) + "..." + accounts[0].slice(37);
  }

  console.log("Button set");
}


//Sets the InnerText button to be pending. 
async function innerTextButtonPending() {
  let button = document.getElementsByClassName('predictButton')[0];
  button.innerText = "Pending..."
}

//Sets the InnerText button to be pending. 
async function innerTextButtonPredict() {
  let button = document.getElementsByClassName('predictButton')[0];
  button.innerText = "Predict"
}

async function predictToast(event) {
  var options = {
    animation : true,
  };

  //Defining toast HTML element. 
  var toastHTMLElement = document.getElementById('predictToast');

  if (event == "pending"){
    toastHTMLElement.innerHTML = 
    `<div class="toast-header">
    <img src="assets/images/favicon.ico" class="m-r-sm" alt="Toast image" height="18" width="18">
    <strong class="me-auto">Binance Smart Chain</strong>
    <small class="text-muted">Just Now</small>
      <span aria-hidden="true">&times;</span>
    </button>
  </div>
  <div class="toast-body" style="text-align: left;">
    Transaction Pending...
  </div>`
  var toastElement = new bootstrap.Toast(toastHTMLElement, options);
  toastElement.show()
  }


  if (event == "completed"){
    toastHTMLElement.innerHTML = 
    `<div class="toast-header">
    <img src="assets/images/favicon.ico" class="m-r-sm" alt="Toast image" height="18" width="18">
    <strong class="me-auto">Binance Smart Chain</strong>
    <small class="text-muted">Just Now</small>
      <span aria-hidden="true">&times;</span>
    </button>
  </div>
  <div class="toast-body" style="text-align: left;">
    Transaction Complete. Prediction made.
  </div>`
  var toastElement = new bootstrap.Toast(toastHTMLElement, options);
  toastElement.show()
  }


  if (event == "Insuffient Balance"){
    toastHTMLElement.innerHTML = 
    `<div class="toast-header">
    <img src="assets/images/favicon.ico" class="m-r-sm" alt="Toast image" height="18" width="18">
    <strong class="me-auto">Binance Smart Chain</strong>
    <small class="text-muted">Just Now</small>
      <span aria-hidden="true">&times;</span>
    </button>
  </div>
  <div class="toast-body" style="text-align: left;">
    Insufficient RHO to make prediction.
  </div>`
  var toastElement = new bootstrap.Toast(toastHTMLElement, options);
  toastElement.show()
  }


}


//Sets the 'connect wallet' button.
async function setButton(){
  await connect(); //Changes the accounts to the most recent one 
  innerTextButton(); //Sets the inner text button
}


/// On document load
document.addEventListener("DOMContentLoaded", function() {

  // Listener for if the 
  ethereum.on('accountsChanged', async () => {
    await connect();
    innerTextButton()
    console.log("Account channged to " + accounts[0])
  });

  ethereum.on('chainChanged', (chainId) => {
    console.log(chainId)
    window.location.reload();
  });


  ethereum.on('disconnect', (error) => {
    console.log("Disconnection")
    console.log(error)
  });

});



async function makePrediction() {
  
  //Connecting to ensure the most up to date variables
  await setButton()

  if(balance > 0) {

    //Creating a prediction
    const prediction = await contract.predict();

    //Setting HTML and toast
    predictToast('pending')
    innerTextButtonPending() //Setting the button as pending.

    //Awaiting the prediction to be complete
    const returned = await prediction.wait(); //waiting for the block to be mined.

    //Retrieving the signature of the transcation for authorisation. 
    const signature = await signer.signMessage(returned.transactionHash);

    const toPost = {
      signature: signature,
      address: accounts[0],
      hash: returned.transactionHash
    }

    //Returning the signature from the prediction. 
    return toPost
  }
  else {
    console.log("Not enough RHO to create prediction");
    predictToast('Insuffient Balance')
    return false
  }
}

async function pullTheData(){ 

    //Ensuring data is updated:
    connect();

    //Retrieving the posting data for authentication.
    const toPost = await makePrediction();

    //The function that runs when the predict button is pushed.
    //Needs to pull the data from the SQL database. Then set all those element id's to them.

    await fetch('http://185.168.193.110/prediction', {
      method: 'POST',
      headers: {
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(toPost)
    }).then(res => res.json())
      .then(res => (requestedData = res));

    console.log(requestedData)

    //COIN 1
    var time_1 = document.getElementById("time_1");
    time_1.innerHTML = requestedData[0].Time.slice(11).slice(0, -3)

    var coin_1 = document.getElementById("coin_1");
    coin_1.innerHTML = `<a href="https://www.binance.com/en/trade/${requestedData[0].Coin_1}_BTC?layout=basic">${requestedData[0].Coin_1}/BTC</a>` //How to change the name. of the element

    var confidence_coin_1 = document.getElementById("confidence_coin_1");
    confidence_coin_1.innerHTML = requestedData[0].Confidence_1 + "%"//Confidence

    var width_coin_1 = document.getElementById("width_coin_1");
    width_coin_1.style.width = requestedData[0].Confidence_1 + "%" //How to change the width of the bar.

    var title_coin_1 = document.getElementById("title_coin_1");
    title_coin_1.innerHTML = `<a href="https://www.binance.com/en/trade/${requestedData[0].Coin_1}_BTC?layout=basic">${requestedData[0].Coin_1}/BTC</a>` //How to change the name. of the element

    var pannel_coin_1 = document.getElementById("pannel_coin_1"); //Problem, how do you get the tradingview ID? 
    var content = `<!-- TradingView Widget BEGIN -->
    <div class="tradingview-widget-container">
      <div id="tradingview_6bfea" style="height: 500px;"></div>
      <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
      <script type="text/javascript">
      new TradingView.widget(
      {
      "autosize": true,
      "symbol": "BINANCE:${requestedData[0].Coin_1}BTC",
      "interval": "1",
      "timezone": "Europe/London",
      "theme": "dark",
      "style": "3",
      "locale": "en",
      "toolbar_bg": "#f1f3f6",
      "enable_publishing": false,
      "hide_legend": true,
      "allow_symbol_change": true,
      "save_image": false,
      "details": true,
      "container_id": "tradingview_6bfea"
    }
      );
      </script>
    </div>
    <!-- TradingView Widget END -->`;

    pannel_coin_1.innerHTML = content;
    var scripts = pannel_coin_1.getElementsByTagName("script"); //refreshing all script tags
    for (var i = 0; i < scripts.length; i++) {
    eval(scripts[i].innerText);
    }

    //COIN 2
    var time_2 = document.getElementById("time_2");
    time_2.innerHTML = requestedData[0].Time.slice(11).slice(0, -3)

    var coin_2 = document.getElementById("coin_2");
    coin_2.innerHTML = `<a href="https://www.binance.com/en/trade/${requestedData[0].Coin_2}_BTC?layout=basic">${requestedData[0].Coin_2}/BTC</a>` //How to change the name. of the element

    var confidence_coin_2 = document.getElementById("confidence_coin_2");
    confidence_coin_2.innerHTML = requestedData[0].Confidence_2 + "%" //Confidence

    var width_coin_2 = document.getElementById("width_coin_2");
    width_coin_2.style.width = requestedData[0].Confidence_2 + "%" //How to change the width of the bar.

    var title_coin_2 = document.getElementById("title_coin_2");
    title_coin_2.innerHTML = `<a href="https://www.binance.com/en/trade/${requestedData[0].Coin_2}_BTC?layout=basic">${requestedData[0].Coin_2}/BTC</a>` //How to change the name. of the element

    var pannel_coin_2 = document.getElementById("pannel_coin_2"); //Problem, how do you get the tradingview ID? 
    var content = `<!-- TradingView Widget BEGIN -->
    <div class="tradingview-widget-container">
      <div id="tradingview_1dbf7" style="height: 300px;"></div>
      <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
      <script type="text/javascript">
      new TradingView.widget(
      {
      "autosize": true,
      "symbol": "BINANCE:${requestedData[0].Coin_2}BTC",
      "timezone": "Europe/London",
      "theme": "dark",
      "style": "3",
      "locale": "en",
      "toolbar_bg": "#f1f3f6",
      "enable_publishing": false,
      "hide_legend": true,
      "range": "1D",
      "save_image": false,
      "allow_symbol_change": true,
      "container_id": "tradingview_1dbf7"
    }
      );
      </script>
    </div>
    <!-- TradingView Widget END -->`;

    pannel_coin_2.innerHTML = content;
    var scripts = pannel_coin_2.getElementsByTagName("script"); //refreshing all script tags
    for (var i = 0; i < scripts.length; i++) {
    eval(scripts[i].innerText);
    }

    //COIN 3
    var time_3 = document.getElementById("time_3");
    time_3.innerHTML = requestedData[0].Time.slice(11).slice(0, -3)

    var coin_3 = document.getElementById("coin_3");
    coin_3.innerHTML = `<a href="https://www.binance.com/en/trade/${requestedData[0].Coin_3}_BTC?layout=basic">${requestedData[0].Coin_3}/BTC</a>` //How to change the name. of the element

    var confidence_coin_3 = document.getElementById("confidence_coin_3");
    confidence_coin_3.innerHTML = requestedData[0].Confidence_3 + "%" //Confidence

    var width_coin_3 = document.getElementById("width_coin_3");
    width_coin_3.style.width = requestedData[0].Confidence_3 + "%" //How to change the width of the bar.
    
    var title_coin_3 = document.getElementById("title_coin_3");
    title_coin_3.innerHTML = `<a href="https://www.binance.com/en/trade/${requestedData[0].Coin_3}_BTC?layout=basic">${requestedData[0].Coin_3}/BTC</a>` //How to change the name. of the element

    var pannel_coin_3 = document.getElementById("pannel_coin_3"); //Problem, how do you get the tradingview ID? 
    var content = `<!-- TradingView Widget BEGIN -->
    <div class="tradingview-widget-container">
      <div id="tradingview_cc910" style="height: 300px;"></div>
      <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
      <script type="text/javascript">
      new TradingView.widget(
      {
      "autosize": true,
      "symbol": "BINANCE:${requestedData[0].Coin_3}BTC",
      "timezone": "Europe/London",
      "theme": "dark",
      "style": "3",
      "locale": "en",
      "toolbar_bg": "#f1f3f6",
      "enable_publishing": false,
      "hide_legend": true,
      "range": "1D",
      "save_image": false,
      "allow_symbol_change": true,
      "container_id": "tradingview_cc910"
    }
      );
      </script>
    </div>
    <!-- TradingView Widget END -->`;

    pannel_coin_3.innerHTML = content;
    var scripts = pannel_coin_3.getElementsByTagName("script"); //refreshing all script tags
    for (var i = 0; i < scripts.length; i++) {
    eval(scripts[i].innerText);
    }


    //COIN 4
    var time_4 = document.getElementById("time_4");
    time_4.innerHTML = requestedData[0].Time.slice(11).slice(0, -3)

    var coin_4 = document.getElementById("coin_4");
    coin_4.innerHTML = `<a href="https://www.binance.com/en/trade/${requestedData[0].Coin_4}_BTC?layout=basic">${requestedData[0].Coin_4}/BTC</a>` //How to change the name. of the element

    var confidence_coin_4 = document.getElementById("confidence_coin_4");
    confidence_coin_4.innerHTML = requestedData[0].Confidence_4 + "%" //Confidence

    var width_coin_4 = document.getElementById("width_coin_4");
    width_coin_4.style.width = requestedData[0].Confidence_4 + "%" //How to change the width of the bar.

    var title_coin_4 = document.getElementById("title_coin_4");
    title_coin_4.innerHTML = `<a href="https://www.binance.com/en/trade/${requestedData[0].Coin_4}_BTC?layout=basic">${requestedData[0].Coin_4}/BTC</a>` //How to change the name. of the element

    var pannel_coin_4 = document.getElementById("pannel_coin_4"); //Problem, how do you get the tradingview ID? 
    var content = `<!-- TradingView Widget BEGIN -->
    <div class="tradingview-widget-container">
      <div id="tradingview_d3bac" style="height: 300px;"></div>
      <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
      <script type="text/javascript">
      new TradingView.widget(
      {
      "autosize": true,
      "symbol": "BINANCE:${requestedData[0].Coin_4}BTC",
      "timezone": "Europe/London",
      "theme": "dark",
      "style": "3",
      "locale": "en",
      "toolbar_bg": "#f1f3f6",
      "enable_publishing": false,
      "hide_legend": true,
      "range": "1D",
      "save_image": false,
      "allow_symbol_change": true,
      "container_id": "tradingview_d3bac"
    }
      );
      </script>
    </div>
    <!-- TradingView Widget END -->`;

    pannel_coin_4.innerHTML = content;
    var scripts = pannel_coin_4.getElementsByTagName("script"); //refreshing all script tags
    for (var i = 0; i < scripts.length; i++) {
    eval(scripts[i].innerText);
    }

    predictToast('completed')
    innerTextButtonPredict() //Setting the button back to predict. 
    setButton(); //setting the balance of the top balance back
}
