from fastapi import FastAPI
from core.management import session_manager
from core.server import async_server
import asyncio

class APIManager:
    def __init__(self, session_mngr: session_manager.SessionManager, address: str):
        self.session_manager = session_mngr
        self.address = address
        self.api = None
        self.server = None
        self.server_task = None

    def start(self):
        self.api = FastAPI()
        self.server = async_server.AsyncServer(address=self.address, session_manager=self.session_manager)
        self.server_task = asyncio.create_task(self.server.start())

    def stop(self):
        self.api = None
        if self.server_task:
            self.server_task.cancel()
        if self.server:
            asyncio.create_task(self.server.stop())

api_manager = APIManager(session_mngr=session_manager.SessionManager(), address="0.0.0.0:8080")
