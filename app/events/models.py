"""Models for locations application"""

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import MetaData
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
        return "Event # {} with type_id {} for dog_id {}".format(self.id, self.event_type_id, self.dog_id)


EventMapping = Table('event', metadata,
                     Column('id', Integer, primary_key=True),
                     Column('datetime', DateTime(timezone=True)),
                     Column('description', Text),
                     Column('expenditure_id', ForeignKey('expenditure.id')),
                     Column('event_type_id', ForeignKey('event_type.id')),
                     Column('dog_id', ForeignKey('dog.id'))
                     )

mapper(Event, EventMapping)
