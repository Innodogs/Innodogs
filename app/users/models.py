"""Models for user's app"""
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import MetaData
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy.orm import mapper

__author__ = 'Xomak'

metadata = MetaData()


class User:
    """User's model"""

    def __init__(self):
        super().__init__()
        self.id = None
        self.is_volunteer = None
        self.is_admin = None
        self.name = None
        self.email = None
        self.password_hash = None

    def __str__(self):
        return "User # %s (%s)" % (self.id, self.name)


UserMapping = Table('user', metadata,
                    Column('id', Integer, primary_key=True),
                    Column('is_volunteer', Boolean),
                    Column('is_admin', Boolean),
                    Column('name', String(100)),
                    Column('email', String(255)),
                    Column('password_hash', String(255)),
                    )

mapper(User, UserMapping)
