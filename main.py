# main.py

from core.models import Identity, Room
from core.events import EventBus, MessageCreated
from core.message_service import MessageService
from storage.local_store import LocalStore

# Setup
event_bus = EventBus()
store = LocalStore()

# Subscribe storage to message events
event_bus.subscribe(MessageCreated, store.handle_message_created)

# Domain setup
identity = Identity.create()
room = Room.create("emergency-room")

# Message service
message_service = MessageService(event_bus)

# Create messages
message_service.create_message(
    room_id=room.room_id,
    sender_id=identity.node_id,
    content="Is anyone there?"
)

message_service.create_message(
    room_id=room.room_id,
    sender_id=identity.node_id,
    content="We need help at sector 8."
)

# Load messages from DB
messages = store.get_messages_for_room(room.room_id)
for m in messages:
    print(m)