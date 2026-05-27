from .encrypter import encrypt, decrypt
from colorama import Fore
import struct

def recv_exact(conn, n):
    data = b""
    while len(data) < n:
        chunk = conn.recv(n - len(data))
        if not chunk:
            raise ConnectionError("Connection closed while receiving data")
        data += chunk
    return data

def send_data(conn, data: bytes):
    enc = encrypt(data)
    conn.sendall(struct.pack('>I', len(enc)))
    conn.sendall(enc)

def recv_data(conn, decode=True):
    try:
        size_data = recv_exact(conn, 4)
        size = struct.unpack('>I', size_data)[0]
        enc = recv_exact(conn, size)
        dec = decrypt(enc)
        return dec.decode() if decode else dec
    except ConnectionError:
        print(Fore.LIGHTRED_EX + "[-] Session Closed!")
        raise
    except Exception as e:
        print(Fore.LIGHTRED_EX + f"[!] Error: {e}")
        raise
