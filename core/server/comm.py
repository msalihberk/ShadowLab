import json
import socket
import struct

from core.crypto.encrypter import encrypt, decrypt
from core.server.protocol import encode_json, decode_json


def recv_exact(conn: socket.socket, size: int) -> bytes:
    data = b""
    while len(data) < size:
        chunk = conn.recv(size - len(data))
        if not chunk:
            raise ConnectionError("Connection closed while receiving data")
        data += chunk
    return data


def send_data(conn: socket.socket, data: bytes | str | dict):
    if isinstance(data, dict):
        payload = encode_json(data)
    elif isinstance(data, str):
        payload = data.encode("utf-8")
    elif isinstance(data, (bytes, bytearray)):
        payload = bytes(data)
    else:
        raise TypeError(f"Unsupported data type: {type(data)!r}")

    enc = encrypt(payload)
    conn.sendall(struct.pack(">I", len(enc)))
    conn.sendall(enc)


def recv_data(conn: socket.socket, decode: bool = True):
    size_data = recv_exact(conn, 4)
    size = struct.unpack(">I", size_data)[0]
    enc = recv_exact(conn, size)
    dec = decrypt(enc)
    if decode:
        return dec.decode("utf-8")
    return dec


def send_json(conn: socket.socket, data):
    send_data(conn, encode_json(data))


def recv_json(conn: socket.socket):
    return decode_json(recv_data(conn, decode=False))
