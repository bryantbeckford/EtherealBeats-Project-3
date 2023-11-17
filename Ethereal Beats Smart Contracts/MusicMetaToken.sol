// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract MusicMetaToken is ERC20 {
    constructor(uint256 initialSupply) ERC20("MusicMetaToken", "MMT") {
        // Initialize contract with initial supply, if needed
        _mint(msg.sender, initialSupply);
    }
}

