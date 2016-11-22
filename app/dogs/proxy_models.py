__author__ = 'Xomak'


class DogWithEvents:
    """
    Proxy model for dog with events in his history
    """

    def __init__(self, dog):
        self.dog = dog
        self.events = []

    def add_event(self, event):
        self.events.append(event)

    def __cmp__(self, other):
        return self.dog == other.dog


class DogWithSignificantEvents(DogWithEvents):
    """
    Proxy model for dog with significant events in his history
    """
    pass


