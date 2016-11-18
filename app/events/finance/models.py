from sqlalchemy import Column
from sqlalchemy import DateTime, Text
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


class InpaymentAndExpenditure:
    def __init__(self):
        super().__init__()
        self.id = None
        self.amount = None
        self.datetime = None
        self.comment = None
        self.user_id = None
        self.type = None


class Expenditure:
    """Standalone expenditure"""

    def __init__(self):
        super().__init__()
        self.id = None
        self.amount = None
        self.datetime = None
        self.comment = None

    def __str__(self):
        return "Expenditure # {} (amount={})".format(self.id, self.amount)


InpaymentAndExpenditureMapping = Table('finance_event', metadata,
                                       Column('id', Integer, primary_key=True),
                                       Column('amount', Numeric()),
                                       Column('datetime', DateTime()),
                                       Column('comment', Text()),
                                       Column('user_id', ForeignKey('user.id')),
                                       Column('type', Text(), primary_key=True)
                                       )

mapper(InpaymentAndExpenditure, InpaymentAndExpenditureMapping)

InpaymentMapping = Table('inpayment', metadata,
                         Column('id', Integer, primary_key=True),
                         Column('amount', Numeric()),
                         Column('datetime', DateTime()),
                         Column('comment', Text()),
                         Column('user_id', ForeignKey('user.id'))
                         )

mapper(Inpayment, InpaymentMapping)

ExpenditureMapping = Table('expenditure', metadata,
                           Column('id', Integer, primary_key=True),
                           Column('amount', Integer),
                           Column('datetime', DateTime()),
                           Column('comment', Text)
                           )

mapper(Expenditure, ExpenditureMapping)
