import json
import uuid
from pydantic import BaseModel
from typing import Optional, Dict, Any

class CommandRequest(BaseModel):
    command: str

class TaskRequest(BaseModel):
    module: str
    action: str
    args: Optional[Dict[str, Any]] = None

def return_all_sessions(sessions: list):
    return {
        "status": "Success",
        "count": len(sessions),
        "agents": [
            {"id": s.id, "address": s.address, "status": s.status}
            for s in sessions
        ]
    }

def create_task(msg_type:str, session_id: str, module: str, action: str, args: dict = None) -> dict:
    """Generates a JSON packet for the agent to execute a task."""
    return {
        "task_id": f"t-{uuid.uuid4().hex[:6]}",
        "session_id": session_id,
        "msg_type": msg_type,
        "module": module,
        "action": action,
        "args": args or {}
    }

def create_response(msg_type:str, task_id: str, status: str, result: dict = None, metadata: dict = None , error: str = None) -> dict:
    """Generates a JSON packet for the agent to send a response."""
    return {
        "task_id": task_id,
        "status": status,
        "msg_type": msg_type,
        "result": result or {},
        "error": error,
        "metadata": metadata or {}
    }
