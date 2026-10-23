import math

class Portfolio:
    def __init__(self):
        self.balance=10000.0
        self.holdings={}

    def buy(self, symbol, quantity, price):
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero")

        if not math.isfinite(price) or price <= 0:
            raise ValueError("Price must be a positive, finite value")

        order_cost = quantity * price

        if self.balance >= order_cost:
            self.balance -= order_cost
            self.holdings[symbol] = self.holdings.get(symbol, 0) + quantity
        else:
            raise ValueError("Insufficient virtual balance")

        return order_cost


    def sell(self, symbol, quantity, price):
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero")
        
        if not math.isfinite(price) or price <= 0:
            raise ValueError("Price must be a positive, finite value")

        available_quantity=self.holdings.get(symbol,0)

        if available_quantity < quantity:
            raise ValueError("Insufficient shares to sell")
         

        sell_value= price*quantity

        remaining_quantity=available_quantity-quantity

        if remaining_quantity==0:
            del self.holdings[symbol]
        else:
            self.holdings[symbol]=remaining_quantity

        self.balance+=sell_value

        return sell_value
    

        

        

        