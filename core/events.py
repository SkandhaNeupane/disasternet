from dataclasses import dataclass
from typing import Any #for event data
from core.models import Message
from typing import Callable, Dict, List, Type

class Event:
    """Base class for all events."""
    pass

@dataclass(frozen=True)
class MessageCreated(Event):
    message: Message

@dataclass(frozen=True)
class MessageReceived(Event):
    message: Message

@dataclass(frozen=True)
class PeerJoined(Event):
    peer_id: str

@dataclass(frozen=True)
class PeerLeft(Event):
    peer_id: str



class EventBus:
    def __init__(self):
        self._handlers: Dict[Type[Event], List[Callable[[Event], None]]] = {}

    def subscribe(self, event_type: Type[Event], handler: Callable[[Event], None]) -> None:
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)

    def publish(self, event:Event) -> None:
        handlers = self._handlers.get(type(event), [])
        for handler in handlers:
            handler(event)