import os
from cryptography.fernet import Fernet


class CryptoManager:

    def __init__(self):
        key = os.getenv("FERNET_KEY")

        if not key:
            raise RuntimeError("FERNET_KEY not set")

        self.fernet = Fernet(key)

    def encrypt(self, data: str) -> str:
        return self.fernet.encrypt(data.encode()).
