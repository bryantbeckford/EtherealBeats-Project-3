// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/audit/2023-03/contracts/token/ERC721/ERC721.sol"; 
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/audit/2023-03/contracts/utils/Counters.sol";

contract EtherealBeatsNFT is ERC721 {

    using Counters for Counters.Counter;

    Counters.Counter private _tokenIdCounter;

    
     struct Song {
        string ipfsHash; // link to off-chain metadata and audio file 
        address payable artist;  
        uint256 royaltyPercent; // e.g. 10 = 10%
    }

    // Struct to store royalty recipient and percentage  
    struct RoyaltyInfo { 
        address recipient;  
        uint24 percentage; // 0-10000 (100% = 10000)  
    }

    // Access rule struct
    struct AccessRule {
        address account; // address granted access  
        uint256 permissions; // bitmask representing access flags  
    }


    mapping(uint256 => Song) public songs;
    mapping(address => uint256[]) public ownerToTokenIds;

    // Royalty info mapping for each tokenId
    mapping(uint256 => RoyaltyInfo[]) public royaltyInfo; 

    // Metadata mappings
    mapping(uint256 => string) private _tokenURIs;  
    mapping(string => bool) private _usedURIs;

    /// Mapping tokenId to access rules array
    mapping(uint256 => AccessRule[]) public accessRules;

    /// Mapping tokenId to metadata CID
    mapping(uint256 => string) public tokenURIs; 

    /// Permission bitmasks
    uint256 public constant PERMISSION_PLAY = 1; 
    uint256 public constant PERMISSION_DOWNLOAD = 2;
    uint256 public constant PERMISSION_REMIX = 4;


    // Event emitted on royalty payout
    event SecondarySaleRoyalties(uint256 tokenId, address recipient, uint256 amount);

    constructor() ERC721("MusicNFT", "MUS") {}
    
    function mint(string memory _ipfsHash) public {
        // Mint new NFT  
         _tokenIdCounter.increment();
        uint256 tokenId = _tokenIdCounter.current();
        
        _mint(msg.sender, tokenId);
        songs[tokenId] = Song({
            ipfsHash: _ipfsHash,
            artist: payable(msg.sender),
            royaltyPercent: 10
        });

        // Set metadata
         _setTokenURI(tokenId, _ipfsHash);
    }

    function _setTokenURI(uint256 tokenId, string memory _tokenURI) internal {
        require(!_usedURIs[_tokenURI], "URI already set");    
        _usedURIs[_tokenURI] = true;
        _tokenURIs[tokenId] = _tokenURI;
    }

    function tokenURI(uint256 tokenId) public view override returns (string memory) {
        return _tokenURIs[tokenId];
    }


    function transfer(uint256 _tokenId, address _to) public {
        // Validate ownership using ownerToTokenIds mapping
        require(ownerToTokenIds[msg.sender][_tokenId] != 0);
        
        // Transfer NFT 
        ownerToTokenIds[msg.sender][_tokenId] = 0;  
        ownerToTokenIds[_to].push(_tokenId);  
    }
    
   
    function setRoyaltyInfo(
        uint256 _tokenId, 
        address _recipient, 
        uint24 _percentage
    ) public {

        // Validate token owner
        require(ownerOf(_tokenId) == msg.sender);
        
        // Validate percentage
        require(_percentage <= 10000, "Max royalty percentage is 10000");

        // Add / update royalty info  
        royaltyInfo[_tokenId].push(
            RoyaltyInfo(_recipient, _percentage)  
        );
    }
    
    function payRoyalties(uint256 _tokenId) public payable {

        // Calculate royalty percentage         
        uint royaltyAmount = msg.value *  
            songs[_tokenId].royaltyPercent / 100;  

        // Pay artist          
        songs[_tokenId].artist.transfer(royaltyAmount); 
    }

    function distributeRoyalties(uint256 _tokenId) internal {

        uint256 profit = msg.value; // Sale price

        // Iterate through recipients and distribute royalties
        for(uint i = 0; i < royaltyInfo[_tokenId].length; i++) {
            
            uint256 amount = (profit * royaltyInfo[_tokenId][i].percentage) / 10000; 

            // Transfer royalties to recipient
            payable(royaltyInfo[_tokenId][i].recipient).transfer(amount); 

            emit SecondarySaleRoyalties(_tokenId, royaltyInfo[_tokenId][i].recipient, amount);
        }
    }

    
    function setAccessRules(
        uint256 _tokenId,
        address _account, 
        uint256 _permissions   
    ) public {
        // Only token owner can set rules
        require(ownerOf(_tokenId) == msg.sender);
        
        // Add rules to array
        accessRules[_tokenId].push(
            AccessRule(_account, _permissions)  
        ); 
    }

    
    function getAccessPermissions(
        uint256 _tokenId,
        address _account
    ) public view returns (uint256) {
     
        // Iterate through rules to check permissions for account 
        for(uint i = 0; i < accessRules[_tokenId].length; i++) {
            if (_account == accessRules[_tokenId][i].account) {
                return accessRules[_tokenId][i].permissions; 
            }
        }
        
        // Default - no permissions
        return 0;
    }

    function checkAccess(
        uint256 _tokenId,
        address _account,
        uint256 _permission
    ) public view returns (bool) {
        // Get permissions bitmap for account
        uint256 permissions = getAccessPermissions(_tokenId, _account); 
        
        // Check if permission bit is set
        return permissions & _permission != 0;
    }

   
}

    



    



