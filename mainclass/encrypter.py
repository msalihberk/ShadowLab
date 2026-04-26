from cryptography.fernet import Fernet
from .system import system

fernet = Fernet(system.getdata("KEY"))

def encrypt(data): return fernet.encrypt(data)
def decrypt(data): return fernet.decrypt(data)

def generate():
    oldData = system.getJson()
    oldData["KEY"] = Fernet.generate_key().decode()
    oldData["authcode"] = Fernet.generate_key().decode()
    
    system.setJson(oldData)