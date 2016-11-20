from flask_wtf import FlaskForm
from wtforms import TextAreaField, SelectField
from wtforms.validators import DataRequired

class LocationsForm(FlaskForm):
    name = TextAreaField('Location name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    parent_id = SelectField('Parent ID', choices=[], coerce=int, validators=[DataRequired()])
