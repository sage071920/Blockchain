from Wallet import Wallet
from Transaction import Transaction
from Blockchain import Blockchain


def main():
    # Walltes für 2 Personen erstllen
    alice = Wallet()
    bob = Wallet()

    # Blockchain erstellen
    chain = Blockchain(difficulty=3)

    # Alice schickt bob 10 münzen, erstellt und signiert mit ihrem key die transaktion
    tx = Transaction(sender=alice.public_key, recipient=bob.public_key, amount=10)
    alice.sign_transaction(tx)
    chain.add_transaction(tx)

    # transaction wird verarbeitet
    print("Mining Block 1 ...")
    chain.mine_pending(miner_address=alice.public_key)
    print("Kette gueltig?", chain.is_chain_valid())

    # Versuch einen betrag nachträglich zu ändern
    chain.chain[1].transactions[0].amount = 9999
    print("Nach Manipulation gueltig?", chain.is_chain_valid())  # erwartet: False


if __name__ == "__main__":
    main()