from core.models import Message
from core.events import EventBus, MessageCreated

class MessageService:
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus

    def create_message(self, room_id: str, sender_id: str, content: str) -> Message:
        message = Message.create(
            room_id=room_id,
            sender_id=sender_id,
            content=content
        )

        self.event_bus.publish(MessageCreated(message=message))
        return message