# src/services/history_service.py
from collections import deque
from src.config import MAX_HISTORY, HISTORY_SPLIT_INDEX

class HistoryService:
    def __init__(self):
        self._channel_history = {}

    def add_to_history(self, channel_id, author_name, content):
        """Adds a new message to the history for a specific channel."""
        if channel_id not in self._channel_history:
            self._channel_history[channel_id] = deque(maxlen=MAX_HISTORY)

        self._channel_history[channel_id].append(f"{author_name}: {content}")

    def get_partitioned_history(self, channel_id):
        """Returns the recent and old parts of the history for a channel."""
        history = list(self._channel_history.get(channel_id, []))

        split_index = max(0, len(history) - HISTORY_SPLIT_INDEX)
        old_chunk = history[:split_index]
        recent_chunk = history[split_index:]

        return old_chunk, recent_chunk

# Singleton instance to be used across the application
history_service = HistoryService()
