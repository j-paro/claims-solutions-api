import os
import hashlib


class Password():
    def __init__(self, plaintext, salt=os.urandom(32)) -> None:
        self.salt = salt
        self.hash = hashlib.pbkdf2_hmac(
            'sha256',
            plaintext.encode('ASCII'),
            self.salt,
            1000000
        )
