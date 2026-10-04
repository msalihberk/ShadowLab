from cryptography.fernet import Fernet
from cli.system import System


_key = System.getdata("KEY", "user_data")
if isinstance(_key, str):
    _key = _key.encode()
fernet = Fernet(_key)

def encrypt(data): return fernet.encrypt(data)
def decrypt(data): return fernet.decrypt(data)

def generate():
    oldData = System.getJson("user_data")
    oldData["KEY"] = Fernet.generate_key().decode()
    oldData["authcode"] = Fernet.generate_key().decode()
    
    System.setJson(oldData, "user_data")