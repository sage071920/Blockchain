from ecdsa import VerifyingKey, SECP256k1, BadSignatureError

import hashlib


class Transaction:
    def __init__(self, sender: str | None, recipient: str, amount: float, asset: str = "CASH"):
        self.sender = sender
        self.asset = asset
        self.recipient = recipient
        self.amount = amount
        self.signature: str | None = None

    def transaction_hash(self) -> str:

        trans_str = f"{self.sender}{self.recipient}{self.amount}{self.asset}"

        trans_bin = trans_str.encode()

        return hashlib.sha256(trans_bin).hexdigest()

    def is_valid(self) -> bool:

        if self.sender is None:
            return True

        if self.signature is None:
            return False

        vk = VerifyingKey.from_string(bytes.fromhex(self.sender), curve=SECP256k1)

        try:
            vk.verify(bytes.fromhex(self.signature), self.transaction_hash().encode())
            return True

        except BadSignatureError:
            return False

    def to_dict(self) -> dict:
        return {
            "sender": self.sender,
            "recipient": self.recipient,
            "amount": self.amount,
            "asset": self.asset,
            "signature": self.signature
        }