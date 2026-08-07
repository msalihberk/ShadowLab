from protocol import *
from session import *
from session_manager import *
import asyncio


class AsyncServer:
    def __init__(self, address: str, session_id: str):
        self.address = address
        self.session_id = session_id
        self.reader = None;
        self.writer = None;

    async def handle_request(self, reader):
        return await recv_data(reader);

    async def start(self):
        asyncio.start_server