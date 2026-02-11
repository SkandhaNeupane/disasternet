from dataclasses import dataclass
from datetime import datetime
import uuid
import hashlib

@dataclass(frozen=True) #creates an immutable class with automatically generated methods (__init__, __repr__, etc.)
class Identity:
    node_id: str
    created_at: datetime

    @staticmethod
    def create() -> "Identity":
        return Identity(
            node_id=str(uuid.uuid4()),
            created_at=datetime.now()
        )


@dataclass
class Room:
    room_id: str
    name: str
    created_at: datetime

    @staticmethod
    def create(name: str) -> "Room":
        return Room(
            room_id=str(uuid.uuid4()),
            name=name,
            created_at=datetime.utcnow()
        )
    


 


@dataclass(frozen=True)
class Message:
    message_id: str
    room_id: str
    sender_id: str
    content: str
    timestamp: datetime
    hash: str

    @staticmethod
    def create(
        room_id: str,
        sender_id: str,
        content: str
    ) -> "Message":
        timestamp = datetime.utcnow()
        raw = f"{room_id}{sender_id}{content}{timestamp}".encode()

        return Message(
            message_id=str(uuid.uuid4()),
            room_id=room_id,
            sender_id=sender_id,
            content=content,
            timestamp=timestamp,
            hash=hashlib.sha256(raw).hexdigest()
        )   