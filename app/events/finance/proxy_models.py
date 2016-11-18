from app.events.finance.models import Inpayment
from app.users.models import User

__author__ = 'Xomak'


class InpaymentWithUserName:

    def __init__(self, inpayment: Inpayment, user: User):
        self.inpayment = inpayment
        self.user = user
