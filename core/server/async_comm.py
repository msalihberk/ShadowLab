import asyncio
import struct
from typing import Any

from colorama import Fore

from core.crypto.encrypter import encrypt, decrypt
from core.server.protocol import decode_json, encode_json


HEADER_SIZE = 4


async def recv_exact(reader: asyncio.StreamReader, size: int) -> bytes:
    try:
        return await reader.readexactly(size)
    except asyncio.IncompleteReadError as exc:
        raise ConnectionError("Connection closed while receiving data") from exc


async def send_data(writer: asyncio.StreamWriter, data: bytes | str):
    if isinstance(data, str):
        data = data.encode("utf-8")

    enc = encrypt(data)
    writer.write(struct.pack(">I", len(enc)))
    writer.write(enc)
    await writer.drain()


async def recv_data(reader: asyncio.StreamReader, decode=True):
    try:
        size_data = await recv_exact(reader, HEADER_SIZE)
        size = struct.unpack(">I", size_data)[0]
        enc = await recv_exact(reader, size)
        dec = decrypt(enc)
        return dec.decode("utf-8") if decode else dec
    except ConnectionError:
        print(Fore.LIGHTRED_EX + "[-] Session Closed!")
        raise
    except Exception as e:
        print(Fore.LIGHTRED_EX + f"[!] Error: {e}")
        raise


async def send_json(writer: asyncio.StreamWriter, data: Any):
    await send_data(writer, encode_json(data))


async def recv_json(reader: asyncio.StreamReader) -> Any:
    # TODO test
    d = await recv_data(reader, decode=False)
    print(d)
    return decode_json(d)


async def async_send(writer: asyncio.StreamWriter, data: Any):
    await send_json(writer, data)


async def async_recv(reader: asyncio.StreamReader) -> Any:
    return await recv_json(reader)
