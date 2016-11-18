"""Models for events"""
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import MetaData
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy import Text
from sqlalchemy.orm import mapper

__author__ = 'mputilov'

metadata = MetaData()


class Event:
    """Associated event for particular dog"""

    def __init__(self):
        super().__init__()
        self.id = None
        self.datetime = None
        self.description = None
        self.expenditure_id = None
        self.event_type_id = None
        self.dog_id = None

    def __str__(self):
        return "Event # {} for Dog # {} ({})".format(self.id, self.dog_id, self.description[:30])


EventMapping = Table('event', metadata,
                     Column('id', Integer, primary_key=True),
                     Column('datetime', DateTime(timezone=True)),
                     Column('description', Text),
                     Column('expenditure_id', ForeignKey('expenditure.id')),
                     Column('event_type_id', ForeignKey('event_type.id')),
                     Column('dog_id', ForeignKey('dog.id'))
                     )

mapper(Event, EventMapping)


class Expenditure:
    """Standalone expenditure"""

    def __init__(self):
        super().__init__()
        self.id = None
        self.amount = None
        self.datetime = None
        self.comment = None

    def __str__(self):
        return "Expenditure # {} (amount={})".format(self.id, self.amount)


ExpenditureEventMapping = Table('expenditure', metadata,
                                Column('id', Integer, primary_key=True),
                                Column('amount', Integer),
                                Column('datetime', DateTime()),
                                Column('comment', Text)
                                )

mapper(Expenditure, ExpenditureEventMapping)


class FinancialEvent(Event):
    """Associated financial event for particular dog"""

    def __init__(self):
        super().__init__()
        self.expenditure = None

    def post_init(self, event: Event, expenditure: Expenditure):
        self.id = event.id
        self.datetime = event.datetime
        self.description = event.description
        self.expenditure_id = event.expenditure_id
        self.event_type_id = event.event_type_id
        self.dog_id = event.dog_id
        self.expenditure = expenditure

    def __str__(self):
        return "FinancialEvent # {} for Dog # {} ({})".format(self.id, self.dog_id, self.description)


class EventType:
    """Event type model"""

    def __init__(self):
        super().__init__()
        self.id = None
        self.type_name = None
        self.is_significant = None

    def __str__(self):
        return "EventType # %s (%s)" % (self.id, self.type_name)


EventTypeMapping = Table('event_type', metadata,
                         Column('id', Integer, primary_key=True),
                         Column('type_name', String(255)),
                         Column('is_significant', Boolean)
                         )

mapper(EventType, EventTypeMapping)
