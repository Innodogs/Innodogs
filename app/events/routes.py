from flask import request
from flask_login import login_required

from app.users.utils import requires_roles
from . import events


@events.route('/edit/<int:event_id>', methods=['GET', 'POST'])
@login_required
@requires_roles('volunteer')
def edit_event(event_id: int):
    if request.method == 'GET':
        return "edit form" + str(event_id)
    elif request.method == 'POST':
        return "updated!"


@events.route('/', methods=['GET', 'POST'])
@login_required
@requires_roles('volunteer')
def new_event():
    if request.method == 'GET':
        return "new form"
    elif request.method == 'POST':
        return "added!"


# todo: исправить потом methods, после подключения javascript который будет пулять правильные методы для реквестов
@events.route('/delete/<int:event_id>', methods=['GET', 'POST'])
@login_required
@requires_roles('volunteer')
def delete_event(event_id: int):
    if request.method == 'GET':
        return "delete form"
    elif request.method == 'POST':
        return "deleted!"
