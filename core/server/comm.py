import socket
import struct


def _recv_exact(conn, size):
    data = b""
    while len(data) < size:
        chunk = conn.recv(size - len(data))
        if not chunk:
            break
        data += chunk
    return data


def send_data(conn, data):
    if isinstance(data, str):
        data = data.encode("utf-8")
    if not isinstance(data, (bytes, bytearray)):
        data = str(data).encode("utf-8")
    size = struct.pack(">I", len(data))
    conn.sendall(size)
    conn.sendall(data)


def recv_data(conn, decode=True):
    size_bytes = _recv_exact(conn, 4)
    if len(size_bytes) < 4:
        raise ConnectionError("connection closed")
    size = struct.unpack(">I", size_bytes)[0]
    data = _recv_exact(conn, size)
    if len(data) < size:
        raise ConnectionError("incomplete payload")
    if decode:
        return data.decode("utf-8", errors="replace")
    return data
