
from backend.routers import health
from backend.schemas import TradeRequest
from fastapi import FastAPI, HTTPException
from backend.services.portfolio import Portfolio

app = FastAPI(title="TradeMind-AI API")

app.include_router(health.router)
app.state.portfolio = Portfolio()


@app.get("/")
def home():
    return {
        "message": "Welcome to TradeMind-AI!",
        "status": "running"
    }


@app.post("/trades")
def create_trade(trade: TradeRequest):
    portfolio = app.state.portfolio
    price = 3000.0

    try:
        if trade.side == "buy":
            order_value = portfolio.buy(
                symbol=trade.symbol,
                quantity=trade.quantity,
                price=price
            )
            message = "Buy order completed"

        else:
            order_value = portfolio.sell(
                symbol=trade.symbol,
                quantity=trade.quantity,
                price=price
            )
            message = "Sell order completed"

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        ) from error

    return {
        "message": message,
        "symbol": trade.symbol,
        "quantity": trade.quantity,
        "side": trade.side,
        "price_per_share": price,
        "order_value": order_value,
        "holdings": portfolio.holdings,
        "remaining_balance": portfolio.balance
    }

def test_invalid_trade_side_is_rejected():
    response = client.post(
        "/trades",
        json={
            "symbol": "AAPL",
            "quantity": 1,
            "side": "hold"
        }
    )

    assert response.status_code == 422

    # Validation should happen before portfolio changes.
    assert app.state.portfolio.balance == 10000.0
    assert app.state.portfolio.holdings == {}
