from Block import Block
from Transaction import Transaction


class Blockchain:
    def __init__(self, difficulty: int = 3):
        self.chain: list[Block] = []
        self.pending: list[Transaction] = []
        self.difficulty = difficulty
        self.create_genesis_block()


    def get_balance(self, address: str, asset: str = "CASH") -> float:

        amount = 0.0
        for block in self.chain:
            for transaction in block.transactions:
                if transaction.asset != asset:
                    continue
                if transaction.sender == address:
                    amount -= transaction.amount
                if transaction.recipient == address:
                    amount += transaction.amount

        return amount


    def create_genesis_block(self) -> None:

        self.chain.append(Block(0, [], "0"))


    def latest_block(self) -> Block:

        return self.chain[-1]


    def add_transaction(self, tx: Transaction) -> None:
        if not tx.is_valid():
            raise ValueError("Transaction is not valid")
        if tx.amount <= 0:
            raise ValueError("Amount must be positive")
        if tx.recipient == tx.sender:
            raise ValueError("Sender and recipient are the same")
        if tx.sender is not None and self.get_balance(tx.sender, tx.asset) < tx.amount:
            raise ValueError("Insufficient balance")
        self.pending.append(tx)


    def fund(self, address: str, amount: float, asset: str = "CASH") -> None:
        tx = Transaction(sender = None, recipient = address, amount = amount, asset=asset)
        self.add_transaction(tx)


    def mine_pending(self, miner_address: str) -> Block:

        self.pending.append(Transaction(sender = None, recipient = miner_address, amount = 0.0))

        new_block = Block(len(self.chain), self.pending, self.latest_block().hash)

        new_block.mine(self.difficulty)

        self.chain.append(new_block)

        self.pending.clear()

        return new_block


    def is_chain_valid(self) -> bool:

        for i in range(1, len(self.chain)):
            block = self.chain[i]
            previous = self.chain[i - 1]
            if block.hash != block.compute_hash():
                return False
            if block.previous_hash != previous.hash:
                return False
        return True
