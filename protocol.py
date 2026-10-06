import json
from dataclasses import dataclass
from typing import Any


@dataclass
class Message:
    type: str
    data: dict[str, Any]

    def to_json(self) -> str:
        """Serialize the message to JSON."""
        return json.dumps({
            "type": self.type,
            "data": self.data,
        })

    @classmethod
    def from_json(cls, raw_message: str) -> "Message":
        """Deserialize a JSON string into a Message."""
        try:
            payload = json.loads(raw_message)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON message") from exc

        if not isinstance(payload, dict):
            raise ValueError("Message must be a JSON object")

        message_type = payload.get("type")
        data = payload.get("data", {})

        if not isinstance(message_type, str):
            raise ValueError("Message 'type' must be a string")

        if not isinstance(data, dict):
            raise ValueError("Message 'data' must be an object")

        return cls(type=message_type, data=data)


def chat_message(message: str) -> Message:
    """Create a chat message."""
    return Message(
        type="chat",
        data={
            "message": message,
        },
    )


def join_message(client_id: str) -> Message:
    """Create a client-joined message."""
    return Message(
        type="join",
        data={
            "client_id": client_id,
        },
    )


def leave_message(client_id: str) -> Message:
    """Create a client-left message."""
    return Message(
        type="leave",
        data={
            "client_id": client_id,
        },
    )
