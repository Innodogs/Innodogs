from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import TextAreaField, BooleanField, SelectField, DateTimeField
from wtforms.validators import DataRequired, Required

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