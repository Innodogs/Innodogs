from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy.orm import mapper
from sqlalchemy.sql.sqltypes import Numeric

metadata = MetaData()


class Inpayment:
    def __init__(self):
        super().__init__()
        self.id = None
        self.amount = None
        self.datetime = None
        self.comment = None
        self.user_id = None


InpaymentMapping = Table('inpayment', metadata,
                         Column('id', Integer, primary_key=True),
                         Column('amount', Numeric()),
                         Column('datetime', DateTime()),
                         Column('comment', DateTime()),
                         Column('user_id', ForeignKey('user.id'))
                         )

mapper(Inpayment, InpaymentMapping)
