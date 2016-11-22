from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired

__author__ = 'Xomak'

class UsersFilterForm(FlaskForm):
    """
    Form for user filtering
    """
    name = StringField("User name")
    is_active = BooleanField("Is active", default=False)
    is_volunteer = BooleanField("Volunteer", default=False)
    is_admin = BooleanField("Admin", default=False)
