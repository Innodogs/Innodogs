
from flask import render_template

from app.eventtype import event_type
from app.eventtype.repository import EventTypeRepository

__author__ = 'Xomak'

@event_type.route('/', methods=['GET'])
#@login_required
def requests_list():
    ev = EventTypeRepository.get_all_event_types()
    return render_template('eventtype/list.html', event_types=ev)

