from flask_wtf import FlaskForm
from wtforms import TextAreaField, RadioField, BooleanField
from wtforms.validators import DataRequired

class EventTypeForm(FlaskForm):
    type_name = TextAreaField('Type name', validators=[DataRequired()])
    is_significant = BooleanField('Is significant', default=False)
    
