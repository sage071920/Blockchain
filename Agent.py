from OrderBook import Order

class Agent:
    def __init__(self, wallet, exchange, buy_below, sell_above):
        self.wallet = wallet
        self.exchange = exchange
        self.buy_below = buy_below
        self.sell_above = sell_above

    def act(self) -> None:
        price = self.exchange.order_book.last_price
        cash = self.exchange.blockchain.get_balance(self.wallet.public_key, "CASH", include_pending=True)
        stock = self.exchange.blockchain.get_balance(self.wallet.public_key, "STOCK", include_pending=True)

        if price is not None:

            if price < self.buy_below and cash >= price:
                self.exchange.place_limit_order(Order(self.wallet.public_key, "buy", price, 1))

            if price > self.sell_above and stock >= 1:
                self.exchange.place_limit_order(Order(self.wallet.public_key, "sell", price, 1))