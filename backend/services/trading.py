def calculate_order_cost(quantity:int, price:float)->float:
    if quantity <= 0:
        raise ValueError("Quantity must be greater than zero")
    
    return quantity*price

def can_afford_trade(balance: float, order_cost: float) -> bool:
    return balance >= order_cost

def validate_buy_order(
    quantity: int,
    price: float,
    balance: float
) -> float:
    order_cost = calculate_order_cost(quantity, price)

    if not can_afford_trade(balance, order_cost):
        raise ValueError("Insufficient virtual balance")

    return order_cost