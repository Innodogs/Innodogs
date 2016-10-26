"""Models for user's app"""
from flask_login import UserMixin
from sqlalchemy import BigInteger
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import MetaData
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy.orm import mapper

__author__ = 'Xomak'

metadata = MetaData()


class User(UserMixin):
    """User's model"""

    def __init__(self, **kwargs):
        super().__init__()
        self.id = None
        self.name = kwargs['name']
        self.google_id = str(kwargs['id'])
        self.is_volunteer = False
        self.is_admin = False
        self.email = kwargs['email']
        self.password_hash = 0

    def get_id(self):
        try:
            return self.google_id
        except AttributeError:
            raise NotImplementedError('No `google_id` attribute - override `get_id`')

    def __str__(self):
        return "User # %s (%s)" % (self.id, self.name)


UserMapping = Table('user', metadata,
                    Column('id', Integer, primary_key=True),
                    Column('google_id', BigInteger),
                    Column('is_volunteer', Boolean),
                    Column('is_admin', Boolean),
                    Column('name', String(100)),
                    Column('email', String(255)),
                    Column('password_hash', String(255)),
                    )

mapper(User, UserMapping)
