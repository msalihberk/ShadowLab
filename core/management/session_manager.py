import asyncio
from typing import Dict, Optional, List
from core.management.session import Session

class SessionManager:
    def __init__(self):
        self.sessions: Dict[int, Session] = {}
        self._lock = asyncio.Lock()

    async def add_session(self, session: Session):
        async with self._lock:
            self.sessions[session.id] = session

    async def remove_session(self, session_id: int):
        async with self._lock:
            session = self.sessions.pop(session_id, None)
            if session:
                try:
                    session.writer.close()
                    await session.writer.wait_closed()
                except Exception:
                    pass

    async def clear_all_sessions(self):
        tasks = [self.remove_session(agent.id) for agent in list(self.sessions.values())]
        if tasks:
            await asyncio.gather(*tasks)

    async def get_session(self, session_id: int) -> Optional[Session]:
        async with self._lock:
            return self.sessions.get(session_id)

    async def get_all_sessions(self) -> List[Session]:
        async with self._lock:
            return list(self.sessions.values())