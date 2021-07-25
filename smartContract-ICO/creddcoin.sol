//credcoin

pragma solidity ^0.4.11;

contract credcoin_ico{
//max coins offered 
    uint public max_creddcoin = 1000000;
//exchange rate 
    uint public dollar_creddcoin = 10;
//total creddcoin bought
    uint public creddcoin_bought = 0;
    
//mapping investor address to dollar equity and creddcoin equity
    mapping(address => uint)equity_creddcoin;
    mapping(address => uint)equity_dollar;
    
    
    modifier can_buy_creddcoin(uint dollar_invested){
        require (dollar_invested * dollar_creddcoin + creddcoin_bought <= max_creddcoin);
        _;
    }
    
//getting the credcoin equity of investor
    function equity_in_creddcoin(address investor) external constant returns(uint){
        return equity_creddcoin[investor];
    }

//getting dollar equity of investor
    function equity_in_dollar(address investor) external constant returns(uint){
        return equity_dollar[investor];
    }   
    
//buying creddcoin 
    function buying_creddcoin(address investor, uint dollar_invested) external can_buy_creddcoin(dollar_invested){
        uint temp_creddcoins = dollar_invested * dollar_creddcoin;
        equity_creddcoin[investor] += temp_creddcoins;
        equity_dollar[investor] -= dollar_invested;
        creddcoin_bought -= temp_creddcoins;
    }
    
//selling creddcoin 
    function selling_creddcoin(address investor, uint creddcoin_sell) external{
        uint temp_dollars = creddcoin_sell / dollar_creddcoin;
        equity_creddcoin[investor] -= creddcoin_sell;
        equity_dollar[investor] += temp_dollars;
        creddcoin_bought -= creddcoin_sell;
    }
}