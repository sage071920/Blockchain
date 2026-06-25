

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

    def _record_trade(self, buyer, seller, price, quantity):
        self.trades.append({"buyer": buyer, "seller": seller, "price": price, "quantity": quantity})
        self.last_price = price

    def place_limit_order(self, order: Order) -> None:
        if order.side == "buy":
            while order.quantity > 0:

                best_ask = self.best_ask()

                if best_ask is None or best_ask.price > order.price:
                    break

                trade_size = min(order.quantity, best_ask.quantity)

                self._record_trade(order.owner, best_ask.owner, best_ask.price, trade_size)

                order.quantity -= trade_size
                best_ask.quantity -= trade_size

                if best_ask.quantity == 0:
                    self.asks.remove(best_ask)

            if order.quantity > 0:
                self.bids.append(order)

        elif order.side == "sell":
            while order.quantity > 0:

                best_bid = self.best_bid()

                if best_bid is None or best_bid.price < order.price:
                    break

                trade_size = min(order.quantity, best_bid.quantity)

                self._record_trade(best_bid.owner, order.owner, best_bid.price, trade_size)

                order.quantity -= trade_size
                best_bid.quantity -= trade_size

                if best_bid.quantity == 0:
                    self.bids.remove(best_bid)

            if order.quantity > 0:
                self.asks.append(order)



