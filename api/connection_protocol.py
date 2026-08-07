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


def encode_message(message: dict) -> str:
    """Serialize a protocol message into a JSON payload."""
    return json.dumps(message, ensure_ascii=False, separators=(",", ":"))


def decode_message(raw_message: str | bytes | bytearray) -> dict:
    """Decode a protocol message into a Python dictionary."""
    if isinstance(raw_message, (bytes, bytearray)):
        raw_message = raw_message.decode("utf-8")
    data = json.loads(raw_message)
    if not isinstance(data, dict):
        raise ValueError("Protocol payload must decode to a JSON object.")
    return data


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
    """Generate a JSON task packet for the agent to execute."""
    return encode_message({
        "type": "task",
        "task_id": f"t-{uuid.uuid4().hex[:6]}",
        "session_id": session_id,
        "module": module,
        "action": action,
        "args": args or {}
    })


def create_response(task_id: str, status: str, result: dict = None, metadata: dict = None, error: str = None) -> str:
    """Generate a JSON response packet for the server/CLI."""
    return encode_message({
        "type": "response",
        "task_id": task_id,
        "status": status,
        "result": result or {},
        "error": error,
        "metadata": metadata or {}
    })
