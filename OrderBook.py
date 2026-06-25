

class Order:
    def __init__(self, owner: str, side: str, price: float, quantity: int):
        self.owner = owner
        self.side = side
        self.price = price
        self.quantity = quantity


class OrderBook:
    def __init__(self):
        self.bids: list[Order] = []
        self.asks: list[Order] = []
        self.last_price = None
        self.trades = []

    def best_bid(self):

        return max(self.bids, key=lambda x: x.price, default=None)

    def best_ask(self):

        return min(self.asks, key=lambda x: x.price, default=None)


