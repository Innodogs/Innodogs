from flask_wtf import FlaskForm

from wtforms import TextAreaField, SelectField
from wtforms.validators import DataRequired, ValidationError

from .repository import LocationsRepository

class LocationsForm(FlaskForm):

    name = TextAreaField('Location name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    parent_id = SelectField('Parent ID', choices=[], coerce=int, validators=[DataRequired()])

    def __init__(self, current_id=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_id = current_id



    def validate_parent_id(form, field):
        if field.data and form.current_id:
            if LocationsRepository.is_cyclic_dependency(form.current_id, field.data):
                #print(str(form.current_id) + " " + str(field.data))
                raise ValidationError('Incorrect parent location')
