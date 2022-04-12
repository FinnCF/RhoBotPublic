const { expect } = require("chai");
const { ethers } = require("hardhat");


describe("Token contract", function () {
  it("Deployment should assign the total supply of tokens to the owner", async function () {
    const [owner] = await ethers.getSigners();

    const Token = await ethers.getContractFactory("Rho");

    const hardhatToken = await Token.deploy();

    const ownerBalance = await hardhatToken.balanceOf(owner.address);
    expect(await hardhatToken.totalSupply()).to.equal(ownerBalance);
  });
});

describe("Transactions", function() {
    it("Should transfer tokens between accounts", async function() {
      const [owner, addr1, addr2] = await ethers.getSigners();
  
      const Token = await ethers.getContractFactory("Rho");
  
      const hardhatToken = await Token.deploy();
  
      // Transfer 50 tokens from owner to addr1
      await hardhatToken.transfer(addr1.address, 50);
      expect(await hardhatToken.balanceOf(addr1.address)).to.equal(50);
  
      // Transfer 50 tokens from addr1 to addr2
      await hardhatToken.connect(addr1).transfer(addr2.address, 50);
      expect(await hardhatToken.balanceOf(addr2.address)).to.equal(50);
    });
  });

describe("Mint by Owner", function() {
    it("Should mint tokens to the message caller, if owner.", async function() {
      const [owner, addr1, addr2] = await ethers.getSigners();
  
      const Token = await ethers.getContractFactory("Rho");
  
      const hardhatToken = await Token.deploy();

      // Measuring owners token balance before (converting to int for safety)
      const ownerBalance = parseInt(await hardhatToken.balanceOf(owner.address));
  
      // Transfer 500 tokens from owner to addr1
      await hardhatToken.mint(owner.address, 500);
      
      //Checking if 500 tokens were added to the owners balance
      expect(await hardhatToken.balanceOf(owner.address)).to.equal(ownerBalance + 500);

    });
});

describe("Burn by Owner", function() {
    it("Should burn tokens to the message caller, if owner.", async function() {
      const [owner, addr1, addr2] = await ethers.getSigners();
  
      const Token = await ethers.getContractFactory("Rho");
  
      const hardhatToken = await Token.deploy();

      // Measuring owners token balance before (converting to int for safety)
      const ownerBalance = parseInt(await hardhatToken.balanceOf(owner.address));
  
      // Transfer 500 tokens from owner to addr1
      await hardhatToken.burn(owner.address, 500);
      
      //Checking if 500 tokens were added to the owners balance
      expect(await hardhatToken.balanceOf(owner.address)).to.equal(ownerBalance - 500);

    });
});

describe("Mint by Other", function() {
    it("Should return an error, as non-owner called.", async function() {
      const [owner, addr1, addr2] = await ethers.getSigners();
  
      const Token = await ethers.getContractFactory("Rho");
  
      const hardhatToken = await Token.deploy();

      //Checking if when called by a non-owner, the mint function would throw an error. 
      await expect(hardhatToken.connect(addr1).mint(addr1.address, 500)).to.be.revertedWith("Ownable: caller is not the owner");

    });
});

describe("Burn by Other", function() {
    it("Should return an error, as non-owner called.", async function() {
        const [owner, addr1, addr2] = await ethers.getSigners();
    
        const Token = await ethers.getContractFactory("Rho");
    
        const hardhatToken = await Token.deploy();
  
        //Checking if when called by a non-owner, the mint function would throw an error. 
        await expect(hardhatToken.connect(addr1).burn(addr1.address, 500)).to.be.revertedWith("Ownable: caller is not the owner");
  
      });
});

describe("Decimal Call", function() {
    it("Should return 0 decimal places.", async function() {
  
      const Token = await ethers.getContractFactory("Rho");
  
      const hardhatToken = await Token.deploy();

      // Measuring owners token balance before (converting to int for safety)
      const decimals = await hardhatToken.decimals();
  
      //Checking if 500 tokens were added to the owners balance
      expect(await hardhatToken.decimals()).to.equal(0);
    });
});

describe("Prediction", function() {
    it("Should burn a single token from the user, and emit a prediction.", async function() {

      const [owner, addr1, addr2] = await ethers.getSigners();

      const Token = await ethers.getContractFactory("Rho");
  
      const hardhatToken = await Token.deploy();

      //Checking if the event was emmited. 
      expect(await hardhatToken.predict()).to.emit(hardhatToken, 'LogPrediction').withArgs(owner.address);
    });
});


  
//test 22