from app.dogs.models import Dog
from app.events.models import EventType, Event

__author__ = 'Xomak'


class EventWithEventType:
    """
    Proxy model to handle event with its type
    """

    def __init__(self, event: Event, event_type: EventType):
        self.event = event
        self.event_type = event_type


class EventWithEventTypeAndDog:
    """
    Proxy model to handle event with its type and dog
    """

    def __init__(self, event: Event, event_type: EventType, dog: Dog):
        self.event = event
        self.event_type = event_type
        self.dog = dog
