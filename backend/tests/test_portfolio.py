from backend.services.portfolio import Portfolio
import pytest


def test_buy_updates_balance_and_holdings():
    portfolio = Portfolio()

    portfolio.buy("AAPL", 3, 3000)

    assert portfolio.balance == 1000.0
    assert portfolio.holdings == {"AAPL": 3}


def test_buy_with_insufficient_balance_does_not_change_portfolio():
    portfolio = Portfolio()

    with pytest.raises(ValueError, match="Insufficient virtual balance"):
        portfolio.buy("AAPL", 5, 3000)

    assert portfolio.balance == 10000.0
    assert portfolio.holdings == {}


def test_buy_with_zero_quantity_is_rejected():
    portfolio = Portfolio()

    with pytest.raises(ValueError):
        portfolio.buy("AAPL", 0, 3000)

    assert portfolio.balance == 10000.0
    assert portfolio.holdings == {}

def test_buy_with_negative_price_is_rejected():
    portfolio = Portfolio()

    with pytest.raises(ValueError):
        portfolio.buy("AAPL",2,-3000)

    assert portfolio.balance==10000.0
    assert portfolio.holdings=={}


def test_buy_with_infinite_price_is_rejected():
    portfolio= Portfolio()

    with pytest.raises(ValueError):
        portfolio.buy("AAPL", 1, float("inf"))

    assert portfolio.balance == 10000.0
    assert portfolio.holdings == {}

def test_sell_updates_balance_and_holdings():
    portfolio = Portfolio()

    portfolio.buy("AAPL",3,3000)

    sell_value=portfolio.sell("AAPL",2,3000)

    assert portfolio.balance== 7000.0
    assert portfolio.holdings=={"AAPL": 1}
    assert sell_value==6000.0

def test_sell_all_shares_removes_symbol():
    portfolio=Portfolio()

    portfolio.buy("AAPL",3,3000)

    portfolio.sell("AAPL",3,3000)

    assert portfolio.balance==10000.0
    assert "AAPL" not in portfolio.holdings

def test_sell_more_shares_than_owned_is_rejected():
    portfolio= Portfolio()

    portfolio.buy("AAPL",3,3000)

    with pytest.raises(ValueError):
        portfolio.sell("AAPL",5,3000)

    assert portfolio.balance==1000.0
    assert portfolio.holdings=={"AAPL":3}





