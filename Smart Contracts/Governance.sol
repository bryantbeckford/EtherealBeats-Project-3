pragma solidity ^0.8.20;

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/governance/Governor.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/governance/extensions/GovernorCountingSimple.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/governance/extensions/GovernorVotes.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/governance/extensions/GovernorVotesQuorumFraction.sol";


contract DAOGovernence is Governor,GovernorCountingSimple,GovernorVotes,GovernorVotesQuorumFraction{
    constructor(IVotes _token)
        Governor("DAOGovernance")
        GovernorVotes(_token)
        GovernorVotesQuorumFraction(4)
    {}
    function votingDelay() public pure override returns (uint256) {
        return 1; // 1 block
    }

    function votingPeriod() public pure override returns (uint256) {
        return 45818; // 1 week
    }
  
    function proposalThreshold() public pure override returns (uint256) {
        return 0;
    }

    // The following functions are overrides required by Solidity.
    function quorum(uint256 blockNumber)
        public
        view
        override(Governor, GovernorVotesQuorumFraction)
        returns (uint256)
    {
        return super.quorum(blockNumber);
    }
}