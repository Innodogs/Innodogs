from datetime import datetime

from flask_login import current_user

from .forms import AddRequestForm
from .models import AddRequest


def add_request_form_to_domain(form: AddRequestForm) -> AddRequest:
    domain = AddRequest()
    domain.description = form.description.data
    domain.datetime = datetime.utcnow()
    domain.status = 'new'
    domain.user_id = current_user.id
    return domain
