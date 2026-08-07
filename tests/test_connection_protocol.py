import json

from api.connection_protocol import create_task, create_response, decode_message, encode_message


def test_create_task_packet_has_protocol_fields():
    packet = create_task("agent-42", "shell", "exec", {"command": "whoami"})
    data = json.loads(packet)

    assert data["type"] == "task"
    assert data["session_id"] == "agent-42"
    assert data["module"] == "shell"
    assert data["action"] == "exec"
    assert data["args"]["command"] == "whoami"


def test_create_response_packet_has_status_and_result():
    packet = create_response("t-123", "success", {"output": "hello"}, {"duration_ms": 10})
    data = json.loads(packet)
 
    assert data["type"] == "response"
    assert data["task_id"] == "t-123"
    assert data["status"] == "success"
    assert data["result"]["output"] == "hello"
    assert data["metadata"]["duration_ms"] == 10


def test_decode_message_round_trip():
    original = {
        "type": "task",
        "task_id": "t-1",
        "session_id": "agent-1",
        "module": "sysinfo",
        "action": "get",
        "args": {}
    }

    encoded = encode_message(original)
    decoded = decode_message(encoded)

    assert decoded == original
