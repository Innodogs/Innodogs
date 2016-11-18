import datetime

from flask_wtf import FlaskForm
from wtforms import TextAreaField, BooleanField, TextField, StringField, DecimalField, DateTimeField
from wtforms.validators import DataRequired, NumberRange, InputRequired


class EventTypeForm(FlaskForm):
    type_name = TextAreaField('Type name', validators=[DataRequired()])
    is_significant = BooleanField('Is significant', default=False)


class ExpenditureForm(FlaskForm):
    amount = DecimalField('Amount', [NumberRange(min=0.1)])
    datetime = DateTimeField('Operation date and time', default=lambda: datetime.datetime.now())
    comment = TextAreaField('comment', [InputRequired()])
