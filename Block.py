import hashlib
import json
import time

from Transaction import Transaction


class Block:
    def __init__(self, index: int, transactions: list[Transaction], previous_hash: str):
        self.index = index
        self.timestamp = time.time()
        self.transactions = list(transactions)
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.compute_hash()

    def compute_hash(self) -> str:

        block_dict = {
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": [tx.to_dict() for tx in self.transactions],
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
        }

        block_str = json.dumps(block_dict, sort_keys=True)

        block_bin = block_str.encode()

        return hashlib.sha256(block_bin).hexdigest()


    def mine(self, difficulty: int) -> None:

        candidate_hash = self.compute_hash()

        while not candidate_hash.startswith("0" * difficulty):
            self.nonce += 1
            candidate_hash = self.compute_hash()

        self.hash = candidate_hash

    def has_valid_transactions(self) -> bool:

        for tx in self.transactions:
            if not tx.is_valid():
                return False
        return True