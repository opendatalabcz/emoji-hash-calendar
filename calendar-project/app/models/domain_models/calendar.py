from typing import List
from app.models.domain_models.event import Event

class Calendar:
    def __init__(self):
        self.events = []

    def add_event(self, event: Event):
        self.events.append(event)

    def get_events(self) -> List[Event]:
        return self.events

    def clear_events(self):
        self.events = []

    def __len__(self):
        return len(self.events)