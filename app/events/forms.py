from datetime import datetime

from flask_wtf import FlaskForm
from sqlalchemy.orm.exc import NoResultFound
from wtforms import TextAreaField, BooleanField, SelectField, DateTimeField, IntegerField
from wtforms.validators import DataRequired, Required, ValidationError, InputRequired

from app.dogs.repository import DogsRepository
from app.events.repository import EventTypeRepository


class EventTypeForm(FlaskForm):
    type_name = TextAreaField('Type name', validators=[DataRequired()])
    is_significant = BooleanField('Is significant', default=False)


class EventForm(FlaskForm):

    event_type_id = SelectField('Event type', choices=[], coerce=int, validators=[DataRequired()])
    datetime = DateTimeField('Event date and time', default=datetime.now, validators=[DataRequired()])
    description = TextAreaField('Description')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        all_types = EventTypeRepository.get_all_event_types()
        self.event_type_id.choices = [(event_type.id, event_type.type_name) for event_type in all_types]


class EventWithDogForm(EventForm):
    dog_id = IntegerField("Dog id", [InputRequired()])

    # Something strange here with number format
    def validate_dog_id(form, field):
        if field.data is not None:
            try:
                dog = DogsRepository.get_dog_by_id(field.data)
            except NoResultFound:
                raise ValidationError('Incorrect dog selected')
