"""Models for addrequests app"""
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import MetaData
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy import Text
from sqlalchemy.orm import mapper

__author__ = 'Xomak'

metadata = MetaData()


class AddRequest:
    """Dog add request model"""

    def __init__(self):
        super().__init__()
        self.id = None
        self.description = None
        self.datetime = None
        self.status = None
        self.comment = None
        self.user = None

    def __str__(self):
        return "Add request # %s (%s)" % (self.id, self.description)


AddRequestMapping = Table('add_request', metadata,
                          Column('id', Integer, primary_key=True),
                          Column('description', Text),
                          Column('datetime', DateTime),
                          Column('status', String(20)),
                          Column('comment', Text),
                          Column('user_id', ForeignKey('user.id'))
                          )

mapper(AddRequest, AddRequestMapping)
