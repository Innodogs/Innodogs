from datetime import datetime
from typing import List

from flask_login import current_user

from app.addrequests.forms import AddRequestForm
from app.addrequests.models import AddRequest
from app.locations.models import Location


def add_request_form_to_domain(form: AddRequestForm) -> AddRequest:
    domain = AddRequest()
    domain.description = form.description.data
    domain.datetime = datetime.utcnow()
    domain.status = 'new'
    domain.user_id = current_user.id
    return domain


def convert_locations_to_select_choices(locations: List[Location]):
    return [(loc.id, loc.name) for loc in locations]