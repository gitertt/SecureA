import os
import json
import base64
import hashlib
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.exceptions import InvalidTag
import secrets

class PasswordManager:
    def __init__(self, master_password):
        self.master_password = master_password.encode()  # 主密码
        self.salt = b'secure_salt_value'  # 可以保存更随机的salt
        self.key = self.generate_key(self.master_password, self.salt)  # 生成加密密钥
        self.file_name = 'passwords.json'  # 用于存储加密密码的文件

    def generate_key(self, password, salt):
        # 使用PBKDF2生成密钥
        kdf = PBKDF2HMAC(
            algorithm=hashlib.sha256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        return base64.urlsafe_b64encode(kdf.derive(password))

    def encrypt_password(self, plaintext_password):
        # 使用AESGCM加密密码
        aesgcm = AESGCM(self.key)
        nonce = os.urandom(12)  # 12字节的随机nonce
        ciphertext = aesgcm.encrypt(nonce, plaintext_password.encode(), None)
        return base64.urlsafe_b64encode(nonce + ciphertext).decode()

    def decrypt_password(self, encrypted_password):
        try:
            encrypted_password_bytes = base64.urlsafe_b64decode(encrypted_password)
            nonce = encrypted_password_bytes[:12]
            ciphertext = encrypted_password_bytes[12:]
            aesgcm = AESGCM(self.key)
            decrypted_password = aesgcm.decrypt(nonce, ciphertext, None)
            return decrypted_password.decode()
        except InvalidTag:
            return "Decryption failed! Invalid password or corrupted data."

    def store_password(self, account, password):
        encrypted_password = self.encrypt_password(password)
        if os.path.exists(self.file_name):
            with open(self.file_name, 'r') as file:
                data = json.load(file)
        else:
            data = {}
        data[account] = encrypted_password

        with open(self.file_name, 'w') as file:
            json.dump(data, file)

    def retrieve_password(self, account):
        if os.path.exists(self.file_name):
            with open(self.file_name, 'r') as file:
                data = json.load(file)
            encrypted_password = data.get(account)
            if encrypted_password:
                return self.decrypt_password(encrypted_password)
            else:
                return f"No password found for {account}"
        else:
            return "No password storage found."

    def generate_strong_password(self, length=16):
        # 生成强密码
        alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_"
        return ''.join(secrets.choice(alphabet) for i in range(length))


# 使用示例
master_password = input("Enter your master password: ")
pm = PasswordManager(master_password)

# 存储新密码
account = input("Enter account name: ")
generated_password = pm.generate_strong_password()
print(f"Generated strong password for {account}: {generated_password}")
pm.store_password(account, generated_password)

# 检索密码
account_to_retrieve = input("Enter account name to retrieve: ")
retrieved_password = pm.retrieve_password(account_to_retrieve)
print(f"Password for {account_to_retrieve}: {retrieved_password}")