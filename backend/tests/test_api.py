
import pytest
from fastapi.testclient import TestClient

from backend.main import app
from backend.services.portfolio import Portfolio


client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_portfolio():
    app.state.portfolio = Portfolio()


def test_home_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Welcome to TradeMind-AI!",
        "status": "running"
    }


def test_buy_trade_endpoint():
    response = client.post(
        "/trades",
        json={
            "symbol": "AAPL",
            "quantity": 2,
            "side": "buy"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["symbol"] == "AAPL"
    assert data["quantity"] == 2
    assert data["side"] == "buy"
    assert data["order_value"] == 6000.0
    assert data["holdings"] == {"AAPL": 2}
    assert data["remaining_balance"] == 4000.0



def test_sell_trade_endpoint():
    # First, buy 3 shares using the API.
    buy_response = client.post(
        "/trades",
        json={
            "symbol": "AAPL",
            "quantity": 3,
            "side": "buy"
        }
    )

    assert buy_response.status_code == 200

    # Then, sell 1 share using the API.
    sell_response = client.post(
        "/trades",
        json={
            "symbol": "AAPL",
            "quantity": 1,
            "side": "sell"
        }
    )

    assert sell_response.status_code == 200

    data = sell_response.json()

    assert data["symbol"] == "AAPL"
    assert data["quantity"] == 1
    assert data["side"] == "sell"
    assert data["order_value"] == 3000.0
    assert data["holdings"] == {"AAPL": 2}
    assert data["remaining_balance"] == 4000.0


def test_sell_more_shares_than_owned():
    response = client.post(
        "/trades",
        json={
            "symbol": "AAPL",
            "quantity": 1,
            "side": "sell"
        }
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Insufficient shares to sell"
    }

    # The failed trade must not change the portfolio.
    assert app.state.portfolio.balance == 10000.0
    assert app.state.portfolio.holdings == {}


def test_trade_with_zero_quantity_is_rejected():
    response = client.post(
        "/trades",
        json={
            "symbol": "AAPL",
            "quantity": 0,
            "side": "buy"
        }
    )

    assert response.status_code == 422

    # The rejected request must not change the portfolio.
    assert app.state.portfolio.balance == 10000.0
    assert app.state.portfolio.holdings == {}

