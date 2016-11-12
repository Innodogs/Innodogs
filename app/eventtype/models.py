"""Models for events types"""

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import MetaData
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy import Boolean
from sqlalchemy.orm import mapper

__author__ = 'Xomak'

metadata = MetaData()


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
