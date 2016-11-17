from app.events.models import EventType, Event

__author__ = 'Xomak'


class EventWithEventType:
    """
    Proxy model to handle event with its type
    """

    def __init__(self, event: Event, event_type: EventType):
        self.event = event
        self.event_type = event_type
