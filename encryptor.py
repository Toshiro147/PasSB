import base64
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet

class Encryptor:
    def __init__(self, master_password):
        self.salt_file = "vault_data/.salt"
        self.key = self._generate_key(master_password)
        self.fernet = Fernet(self.key)

    def _generate_key(self, password: str):
        if not os.path.exists("vault_data"):
            os.makedirs("vault_data")
            
        if os.path.exists(self.salt_file):
            with open(self.salt_file, "rb") as f:
                salt = f.read()
        else:
            salt = os.urandom(16)
            with open(self.salt_file, "wb") as f:
                f.write(salt)

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=480000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key

    def encrypt(self, plain_text: str):
        return self.fernet.encrypt(plain_text.encode()).decode()

    def decrypt(self, encrypted_text: str):
        try:
            return self.fernet.decrypt(encrypted_text.encode()).decode()
        except Exception:
            return None