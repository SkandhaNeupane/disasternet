import sqlite3
from typing import List 
from datetime import datetime

from core.models import Identity, Room, Message

class LocalStore: 
    def __init__(self, db_path: str = "disasternet.db"):
        self.db_path = db_path
        self.__init__db()

    def __init__db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            message_id TEXT PRIMARY KEY,
            room_id TEXT NOT NULL,
            sender_id TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            hash TEXT NOT NULL
        )
        """)

        conn.commit()
        conn.close()
    

    def save_message(self, message: Message) -> None:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute("""
            INSERT INTO messages (
                message_id, room_id, sender_id,
                content, timestamp, hash
            ) VALUES (?, ?, ?, ?, ?, ?)
            """, (
                message.message_id,
                message.room_id,
                message.sender_id,
                message.content,
                message.timestamp.isoformat(),
                message.hash
            ))
            conn.commit()
        except sqlite3.IntegrityError:
            # Duplicate message (already stored)
            pass
        finally:
            conn.close()


    def get_messages_for_room(self, room_id:str) -> List[Message]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
        SELECT message_id, room_id, sender_id,
               content, timestamp, hash
        FROM messages
        WHERE room_id = ?
        ORDER BY timestamp ASC
        """, (room_id,))

        rows = cursor.fetchall() # Fetch all messages for the given room_id
        conn.close()

        messages = []
        for row in rows: # Convert each row to a Message object
            messages.append(Message(
                message_id=row[0],
                room_id=row[1],
                sender_id=row[2],
                content=row[3],
                timestamp=datetime.fromisoformat(row[4]),
                hash=row[5]
            ))

        return messages
    
    def handle_message_created(self, event) -> None:
        self.save_message(event.message)