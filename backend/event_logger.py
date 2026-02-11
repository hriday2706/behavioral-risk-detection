# backend/event_logger.py

import time

# In-memory storage (demo purpose)
EVENT_STORE = {}

def log_event(session_id, user_id, event_type, metadata=None):
    event = {
        "event_type": event_type,
        "timestamp": time.time(),
        "user_id": user_id,
        "metadata": metadata or {}
    }

    if session_id not in EVENT_STORE:
        EVENT_STORE[session_id] = []

    EVENT_STORE[session_id].append(event)

def get_events(session_id):
    return EVENT_STORE.get(session_id, [])
