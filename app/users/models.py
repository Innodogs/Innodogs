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
        self.id = kwargs.get('id')
        self.name = kwargs.get('name')
        self.google_id = str(kwargs.get('google_id'))
        self.is_volunteer = kwargs.get('is_volunteer', False)
        self.is_admin = kwargs.get('is_admin', False)
        self._is_active = kwargs.get('is_active', kwargs.get('_is_active', True))
        self.email = kwargs.get('email')

    @property
    def is_active(self):
        return self._is_active

    def get_roles(self):
        roles = []
        if self.is_volunteer:
            roles.append('volunteer')
        if self.is_admin:
            roles.append('admin')
        return roles

    def get_id(self):  # get_id is called by google_login plugin.
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
                    Column('_is_active', Boolean),
                    Column('name', String(100)),
                    Column('email', String(255))
                    )

mapper(User, UserMapping)
