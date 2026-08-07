import asyncio
from dataclasses import dataclass

@dataclass
class Session:
    id: int
    writer: asyncio.StreamWriter
    reader: asyncio.StreamReader
    address: str
    status: str