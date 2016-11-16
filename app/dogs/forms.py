from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SelectField

__author__ = 'Xomak'


class DogsFilterForm(FlaskForm):
    """
    Form for dogs filter page
    """

    name = StringField("Dog's name")
    sex = SelectField("Sex", choices=(("", "Choose sex of dog"), ("male", "Male"), ("female", "Female")))
    is_adopted = BooleanField("Is adopted")
