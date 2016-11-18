from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import TextAreaField, DateField
from wtforms.fields.core import SelectField
from wtforms.fields.html5 import DateTimeField, IntegerField, DecimalField
from wtforms.fields.simple import HiddenField
from wtforms.validators import DataRequired, NumberRange, InputRequired

from app.users.repository import UsersRepository


class InpaymentEventForm(FlaskForm):
    id = HiddenField('Inpayment id')
    amount = DecimalField('Amount of money', description='How much money was donated',
                          validators=[DataRequired(), NumberRange()], places=0)
    datetime = DateField('When did it happen', description="When", validators=[DataRequired()],
                             default=datetime.today)
    user_id = SelectField('Who did it', choices=[], description="Who is a donor", coerce=int)
    comment = TextAreaField('Commentary', description="Example: thank you, our dear donor!")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_id.choices = [(u.id, u.name) for u in UsersRepository.get_all_users()]


class ExpenditureForm(FlaskForm):
    amount = DecimalField('Amount', [NumberRange(min=0.1)])
    datetime = DateTimeField('Operation date and time', default=lambda: datetime.now())
    comment = TextAreaField('comment', [InputRequired()])