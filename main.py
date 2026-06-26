from Blockchain import Blockchain
from Wallet import Wallet
from OrderBook import OrderBook, Order
from Exchange import Exchange
from Agent import Agent


def zeige_stand(label, benannt, blockchain):
    print(label)
    for name, agent in benannt:
        cash = blockchain.get_balance(agent.wallet.public_key, "CASH")
        stock = blockchain.get_balance(agent.wallet.public_key, "STOCK")
        print(f"   {name:12s}: {cash:7.0f} CASH | {stock:5.0f} STOCK")


def main():
    # System aufbauen
    blockchain = Blockchain(difficulty=3)
    order_book = OrderBook()
    exchange = Exchange(blockchain, order_book)

    # Agenten anlegen
    kaeufer = [Agent(Wallet(), exchange, buy_below=120, sell_above=10**9) for _ in range(2)]
    verkaeufer = [Agent(Wallet(), exchange, buy_below=0, sell_above=80) for _ in range(2)]
    alle = kaeufer + verkaeufer
    benannt = ([(f"Kaeufer {i}", a) for i, a in enumerate(kaeufer)] +
               [(f"Verkaeufer {i}", a) for i, a in enumerate(verkaeufer)])

    # Wallets erstellen und Startkapital verteilen
    for agent in alle:
        exchange.register(agent.wallet)
    for agent in kaeufer:
        blockchain.fund(agent.wallet.public_key, 5000, "CASH")
    for agent in verkaeufer:
        blockchain.fund(agent.wallet.public_key, 50, "STOCK")
    blockchain.mine_pending("miner")
    zeige_stand("Start:", benannt, blockchain)

    # Eroeffnungspreis setzen
    exchange.place_limit_order(Order(verkaeufer[0].wallet.public_key, "sell", 100, 1))
    exchange.place_limit_order(Order(kaeufer[0].wallet.public_key, "buy", 100, 1))
    blockchain.mine_pending("miner")
    print(f"\nEroeffnungspreis: {order_book.last_price}\n")

    # Simulation: in jeder Runde handelt jeder Agent, danach wird gemined
    for runde in range(1, 101):
        for agent in alle:
            agent.act()
        blockchain.mine_pending("miner")
        print(f"Runde {runde}: Preis {order_book.last_price} | "
              f"Trades gesamt {len(order_book.trades)} | "
              f"offene Bids/Asks {len(order_book.bids)}/{len(order_book.asks)}")

    # 6. Endstand und chain Validation
    print()
    zeige_stand("Endstand:", benannt, blockchain)
    print(f"\nKette gueltig: {blockchain.is_chain_valid()}")


if __name__ == "__main__":
    main()