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
        "status": "success",
        "count": len(sessions),
        "agents": [
            {"id": s.id, "address": s.address, "status": s.status}
            for s in sessions
        ]
    }

def create_task(session_id: str, module: str, action: str, args: dict = None) -> str:
    """Generates a JSON packet for the agent to execute a task."""
    return json.dumps({
        "task_id": f"t-{uuid.uuid4().hex[:6]}",
        "session_id": session_id,
        "module": module,
        "action": action,
        "args": args or {}
    })

def create_response(task_id: str, status: str, result: dict = None, metadata: dict = None , error: str = None) -> str:
    """Generates a JSON packet for the agent to send a response."""
    return json.dumps({
        "task_id": task_id,
        "status": status,
        "result": result or {},
        "error": error,
        "metadata": metadata or {}
    })
