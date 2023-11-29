pragma solidity ^0.8.0;

//imports
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v5.0/contracts/token/ERC20/ERC20.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v5.0/contracts/access/Ownable.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v5.0/contracts/token/ERC20/extensions/ERC20Burnable.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v5.0/contracts/token/ERC20/extensions/ERC20Votes.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v5.0/contracts/token/ERC20/extensions/ERC20Permit.sol";

//DAOToken with governance
contract DAOToken is ERC20,ERC20Burnable,Ownable,ERC20Permit,ERC20Votes {
    constructor()
        ERC20("DAOToken","DAO")
        Ownable()
        ERC20Permit("DAOToken")
        {
            //initial amount of tokens for deployer
            _mint(msg.sender,10*10**decimals());
        }
   

    //Minting of DAOToken
    function mint(address to,uint256 amount) public onlyOwner{
        _mint(to,amount);
    }

    //the following functions are overrides required by solidity
    function _update(address from, address to, uint256 value)
        internal
        override(ERC20, ERC20Votes)
    {
        super._update(from, to, value);
    }

    function nonces(address owner)
        public
        view
        override(ERC20Permit, Nonces)
        returns (uint256)
    {
        return super.nonces(owner);
    }
}