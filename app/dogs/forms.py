from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SelectField, IntegerField
from wtforms.validators import Optional

__author__ = 'Xomak'


class DogsFilterForm(FlaskForm):
    """
    Form for dogs filter page
    """

    name = StringField("Dog's name")
    sex = SelectField("Sex", [Optional()], choices=(("", "Choose sex of dog"), ("male", "Male"), ("female", "Female")))
    is_adopted = BooleanField("Is adopted")
    page = IntegerField("Page")
