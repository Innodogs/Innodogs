from flask_wtf.file import FileAllowed, FileField
from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField
from wtforms.validators import DataRequired, Length, ValidationError

from app.locations.repository import LocationsRepository
from app.events.repository import EventTypeRepository
from wtforms import StringField, BooleanField, SelectField, IntegerField
from wtforms.validators import Optional

__author__ = 'Xomak'


class DogsFilterForm(FlaskForm):
    """
    Form for dogs filter page
    """

    name = StringField("Dog's name")
    sex = SelectField("Sex", [Optional()], choices=(("", "Choose sex of dog"), ("male", "Male"), ("female", "Female")))
    location_id = SelectField('Location', [Optional()], choices=[], coerce=int)
    is_adopted = BooleanField("Is adopted")
    page = IntegerField("Page")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        all_locations = LocationsRepository.get_all_locations()
        self.location_id.choices = [(location.id, location.name) for location in all_locations]


def main_picture_must_be_not_deleted(dog_form, main_picture_field):
    if main_picture_field.data and main_picture_field.data in dog_form.deleted_picture_ids.data.split(','):
        raise ValidationError('Main picture is deleted! That is not possible')


def deleted_pictures_format(form, deleted_pictures_field):
    for char in deleted_pictures_field.data:
        if not (char.isdigit() or char == ','):
            raise ValidationError('Violation of deleted picture ids format!')


class DogForm(FlaskForm):
    id = HiddenField('Id')
    name = StringField('Name', description='Name of the dog')
    sex = SelectField('Sex', choices=[('male', 'male'), ('female', 'female'), ('unknown', 'unknown')],
                      default='unknown', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[
        DataRequired(),
        Length(min=4)
    ], description='A comment about the dog')
    is_hidden = BooleanField('Is hidden')
    is_adopted = BooleanField('Is adopted')
    location_id = SelectField('Location', choices=[], coerce=int)
    pictures = FileField('Pictures', description='Pictures of a dog', validators=[
        FileAllowed(['jpg', 'png'], 'Images only!')
    ], render_kw={'multiple': True})
    main_picture_id = HiddenField('Main picture id out of all pictures', validators=[main_picture_must_be_not_deleted])
    deleted_picture_ids = HiddenField('Deleted picture ids', validators=[deleted_pictures_format])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        all_locations = LocationsRepository.get_all_locations()
        self.location_id.choices = [(location.id, location.name) for location in all_locations]

    @property
    def get_list_of_deleted_picture_ids(self):
        return [int(_id) for _id in self.deleted_picture_ids.data.split(',') if _id]

    @property
    def get_main_picture_id(self):
        return int(self.main_picture_id.data)

class EventsForDogForm(FlaskForm):
    id = HiddenField('Id')
    description = TextAreaField('Description', validators=[
        DataRequired(),
        Length(min=4)
    ], description='What is happend')
    event_type_id = SelectField('Event type', choices=[], coerce=int)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        all_event_types = EventTypeRepository.get_all_event_types()
        self.event_type_id.choices = [(event_type.id, event_type.type_name) for event_type in all_event_types]

