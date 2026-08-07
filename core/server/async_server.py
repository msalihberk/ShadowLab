import asyncio
from core.management.session import Session
from core.management.session_manager import SessionManager
from core.server import async_comm

class AsyncServer:
    def __init__(self, address: str, session_manager: SessionManager):
        self.address = address
        self.session_manager = session_manager
        self.current_id = 1
        self.server = None

    async def handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        client_addr = writer.get_extra_info('peername')
        addr_str = f"{client_addr[0]}:{client_addr[1]}" if client_addr else "Unknown"

        # Add new session to SessionManager
        session_id = self.current_id
        self.current_id += 1

        session = Session(
            id=session_id,
            writer=writer,
            reader=reader,
            address=addr_str,
            status="active"
        )
        await self.session_manager.add_session(session)
        print(f"[+] New agent connected! ID: {session_id} Address: {addr_str}")

        # Listen for incoming messages from the agent
        try:
            while True:
                data = await async_comm.async_recv(reader)
                print(f"[{session_id}] Received data: {data}")
        except Exception as e:
            print(f"[-] Connection lost with agent {session_id} Error: {e}")
        finally:
            # Disconnect the agent and remove the session
            await self.session_manager.remove_session(session_id)

    async def start(self):
        host, port = self.address.split(":")
        self.server = await asyncio.start_server(self.handle_client, host, int(port))
        print(f"[*] C2 Listener active on {self.address}")
        async with self.server:
            await self.server.serve_forever()

    async def stop(self):
        if self.server:
            self.server.close()
            await self.server.wait_closed()

        await self.session_manager.clear_all_sessions()


