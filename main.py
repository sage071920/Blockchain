from Wallet import Wallet
from Transaction import Transaction
from Blockchain import Blockchain


def main():
    # Walltes für 2 Personen erstllen
    alice = Wallet()
    bob = Wallet()

    # Blockchain erstellen
    chain = Blockchain(difficulty=3)

    chain.fund(alice.public_key, 1000)
    chain.fund(bob.public_key, 100)
    chain.mine_pending(miner_address="")

    print("alice Guthaben", chain.get_balance(alice.public_key))

    # Alice schickt bob 10 münzen, erstellt und signiert mit ihrem key die transaktion
    tx = Transaction(sender=alice.public_key, recipient=bob.public_key, amount=10)
    alice.sign_transaction(tx)
    chain.add_transaction(tx)

    # transaction wird verarbeitet
    print("Mining Block 1 ...")
    chain.mine_pending(miner_address=alice.public_key)
    print("Kette gueltig?", chain.is_chain_valid())

    print("alice Guthaben", chain.get_balance(alice.public_key))
    print("bob guthaben", chain.get_balance(bob.public_key))

    # Versuch einen betrag nachträglich zu ändern
    chain.chain[1].transactions[0].amount = 9999
    print("Nach Manipulation gueltig?", chain.is_chain_valid())  # erwartet: False


if __name__ == "__main__":
    main()