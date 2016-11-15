from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import TextAreaField, StringField, SelectField, BooleanField
from wtforms.fields.simple import HiddenField
from wtforms.validators import DataRequired, Length

from app.locations.repository import LocationsRepository


class AddRequestForm(FlaskForm):
    description = TextAreaField('Description', validators=[
        DataRequired(),
        Length(min=4)
    ])
    pictures = FileField('Pictures', validators=[
        FileAllowed(['jpg', 'png'], 'Images only!')
    ])


class RejectRequestForm(FlaskForm):
    comment = TextAreaField('Comment', validators=[DataRequired()])


class ApproveRequestForm(FlaskForm):
    name = StringField('Name', description='Name of the dog')
    sex = SelectField('Sex', choices=[('male', 'male'), ('female', 'female'), ('unknown', 'unknown')],
                      default='unknown', validators=[
            DataRequired()
        ])
    description = TextAreaField('Description', validators=[
        DataRequired(),
        Length(min=4)
    ], description='A comment about the dog')
    is_hidden = BooleanField('Is hidden', validators=[
        # DataRequired()
    ])
    is_adopted = BooleanField('Is adopted', validators=[
        # DataRequired()
    ])
    location_id = SelectField('Location', choices=[], coerce=int)
    main_picture_id = HiddenField('Main picture id out of all pictures')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        all_locations = LocationsRepository.get_all_locations()
        self.location_id.choices = [(location.id, location.name) for location in all_locations]
