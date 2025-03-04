from cryptography.fernet import Fernet
import os
import json
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class ConfigManager:
    def __init__(self):
        self.config_file = 'config.enc'
        self.salt_file = '.salt'
        self._ensure_salt()
        
    def _ensure_salt(self):
        if not os.path.exists(self.salt_file):
            salt = os.urandom(16)
            with open(self.salt_file, 'wb') as f:
                f.write(salt)
    
    def _get_key(self, master_password):
        with open(self.salt_file, 'rb') as f:
            salt = f.read()
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000
        )
        key = base64.urlsafe_b64encode(kdf.derive(master_password.encode()))
        return key
    
    def save_credentials(self, username, password, master_password):
        key = self._get_key(master_password)
        f = Fernet(key)
        
        data = {
            'username': username,
            'password': password
        }
        
        encrypted_data = f.encrypt(json.dumps(data).encode())
        with open(self.config_file, 'wb') as file:
            file.write(encrypted_data)
            
    def load_credentials(self, master_password):
        if not os.path.exists(self.config_file):
            return None, None
            
        key = self._get_key(master_password)
        f = Fernet(key)
        
        try:
            with open(self.config_file, 'rb') as file:
                encrypted_data = file.read()
            
            decrypted_data = f.decrypt(encrypted_data)
            data = json.loads(decrypted_data.decode())
            
            return data['username'], data['password']
        except Exception:
            return None, None 