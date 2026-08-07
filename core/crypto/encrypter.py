from cryptography.fernet import Fernet
from cli.system import system


_key = system.getdata("KEY")
if isinstance(_key, str):
    _key = _key.encode()
fernet = Fernet(_key)

def encrypt(data): return fernet.encrypt(data)
def decrypt(data): return fernet.decrypt(data)

def generate():
    oldData = system.getJson("user_data")
    oldData["KEY"] = Fernet.generate_key().decode()
    oldData["authcode"] = Fernet.generate_key().decode()
    
    system.setJson(oldData, "user_data")