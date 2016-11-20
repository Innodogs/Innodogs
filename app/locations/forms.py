from flask_wtf import FlaskForm
from wtforms import TextAreaField, IntegerField
from wtforms.validators import DataRequired

class LocationsForm(FlaskForm):
    name = TextAreaField('Location name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    parent_id = IntegerField('Parent ID', validators=[DataRequired()])
