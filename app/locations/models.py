"""Models for locations application"""

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import MetaData
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy import Text
from sqlalchemy.orm import mapper

__author__ = 'Xomak'

metadata = MetaData()


class Location:
    """Location model"""

    def __init__(self):
        super().__init__()
        self.id = None
        self.name = None
        self.description = None
        self.parent_id = None

    def __str__(self):
        return "Location # %s (%s)" % (self.id, self.name)


LocationMapping = Table('location', metadata,
                        Column('id', Integer, primary_key=True),
                        Column('name', String(255)),
                        Column('description', Text),
                        Column('parent_id', ForeignKey('location.id'))
                        )

mapper(Location, LocationMapping)
