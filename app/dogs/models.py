"""Models for dogs application"""
import validators
from flask import url_for
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
        # These fields are not presented in the model in case it was initialized by SQLAlchemy
        self.location = None
        self.event_list = None  # non financial
        self.financial_event_list = None
        self.main_picture = None
        self.pictures = None

    def __str__(self):
        return "Dog # %s (%s)" % (self.id, self.name)

    def __cmp__(self, other):
        if other is not Dog:
            return False
        return self.id == other.id


class DogPicture:
    """DogPicture model"""

    def __init__(self, **kwargs):
        self.id = kwargs.get('id', None)
        self.request_id = kwargs.get('request_id', None)
        self.dog_id = kwargs.get('dog_id', None)
        self.uri = kwargs.get('uri', None)
        self.is_main = kwargs.get('is_main', None)

    @property
    def resolved_uri(self):
        if validators.url(self.uri):
            return self.uri
        return url_for('static', filename=self.uri)  # must be local resource in static folder


DogMapping = Table('dog', metadata,
                   Column('id', Integer, primary_key=True),
                   Column('is_hidden', Boolean),
                   Column('name', String(255)),
                   Column('sex', String(10)),
                   Column('is_adopted', Boolean),
                   Column('description', Text),
                   Column('location_id', ForeignKey('location.id'))
                   )

DogPictureMapping = Table('dog_picture', metadata,
                          Column('id', Integer, primary_key=True),
                          Column('request_id', Integer),
                          Column('dog_id', Integer),
                          Column('uri', String(255)),
                          Column('is_main', Boolean)
                          )

mapper(Dog, DogMapping)
mapper(DogPicture, DogPictureMapping)
