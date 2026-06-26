from Transaction import Transaction


class Exchange:
    def __init__(self, blockchain):
        self.blockchain = blockchain

    def settle_trade(self, trade, buyer_wallet, seller_wallet) -> None:

        seller = trade["seller"]
        buyer = trade["buyer"]
        price = trade["price"]
        quantity = trade["quantity"]

        if self.blockchain.get_balance(buyer, "CASH") >= price*quantity and self.blockchain.get_balance(seller, "STOCK") >= quantity:
            cash_transaction = Transaction(sender=buyer, recipient=seller, amount=price*quantity, asset="CASH")
            buyer_wallet.sign_transaction(cash_transaction)
            stock_transaction = Transaction(sender=seller, recipient=buyer, amount=quantity, asset="STOCK")
            seller_wallet.sign_transaction(stock_transaction)

            self.blockchain.add_transaction(cash_transaction)
            self.blockchain.add_transaction(stock_transaction)

        else:
            raise ValueError("Insufficient balance for trade settlement")
