"""Models for dogs application"""
import enum

from sqlalchemy import Boolean
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


class Dog:
    """Dog model"""

    def __init__(self):
        super().__init__()
        self.id = None
        self.is_hidden = None
        self.name = None
        self.sex = None
        self.description = None
        self.is_adopted = None
        self.location_id = None
        self.location = None

    def __str__(self):
        return "Dog # %s (%s)" % (self.id, self.name)

DogMapping = Table('dog', metadata,
                   Column('id', Integer, primary_key=True),
                   Column('is_hidden', Boolean),
                   Column('name', String(255)),
                   Column('sex', String(10)),
                   Column('is_adopted', Boolean),
                   Column('description', Text),
                   Column('location_id', ForeignKey('location.id'))
                   )

mapper(Dog, DogMapping)
