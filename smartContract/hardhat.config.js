require("@nomiclabs/hardhat-waffle");
require("@nomiclabs/hardhat-etherscan");

const ARB_ADDRESS = ""
const ARB_PRIVATE_KEY = ''
const ALCHEMY_API_KEY = "";

/**
 * @type import('hardhat/config').HardhatUserConfig
 */
module.exports = {
  solidity: "0.8.9",
  networks: {
    arbitrum: {
      url: `https://arb-rinkeby.g.alchemy.com/v2/${ALCHEMY_API_KEY}`, //URL with projectID
      accounts: [`${ARB_PRIVATE_KEY}`]
    }
  },
  etherscan: {
    // Your API key for Etherscan
    // Obtain one at https://etherscan.io/
    apiKey: ""
  }
};

//For deployment 
// npx hardhat run scripts/deploy.js --network arbitrum

//For verification
// npx hardhat verify --network arbitrum 0xa01A88D21F2C1264F37316d3e101345DB5c3e898