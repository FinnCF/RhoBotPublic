pragma solidity 0.8.9;

import '@openzeppelin/contracts/access/Ownable.sol';
import '@openzeppelin/contracts/token/ERC20/ERC20.sol';
import "hardhat/console.sol";

contract Rho is Ownable, ERC20 {

    event LogPrediction(address _address);

    constructor () ERC20("RhoBot", 'RHO'){
        _mint(msg.sender, 10000);
    }

    function mint(address account, uint256 amount) public onlyOwner {
        _mint(account, amount);
    }

    function burn(address account, uint256 amount) public onlyOwner {
        _burn(account, amount);
    }

    function decimals() public view virtual override returns (uint8) {
        return 0;
    }

    function predict() external {
        //Transfering the owner a singular Rho token.
        transfer(owner(), 1);

        //Emiting an event for the prediction (to be picked up by api)
        emit LogPrediction(msg.sender);
    }
}