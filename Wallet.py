from ecdsa import SigningKey, SECP256k1

from Transaction import Transaction


class Wallet:
    def __init__(self):
        self.private_key: SigningKey | None = None
        self.public_key: str | None = None
        self.generate_keys()

    def generate_keys(self) -> None:

        sk = SigningKey.generate(curve=SECP256k1) # secret key

        pk = sk.get_verifying_key()               # public key

        public_key_hex = pk.to_string().hex()     # public key als string

        self.private_key = sk
        self.public_key = public_key_hex


    def sign_transaction(self, tx: Transaction) -> None:

        if tx.sender == self.public_key:
            signature = self.private_key.sign(tx.transaction_hash().encode())
            tx.signature = signature.hex()
        else:
            raise PermissionError("sender string doesn't match public key")