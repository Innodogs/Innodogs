from flask import abort, url_for
from flask import redirect
from flask import render_template
from flask import request
from flask_login import login_required
from sqlalchemy.orm.exc import NoResultFound

from app.users.utils import requires_roles
from . import events
from .forms import EventTypeForm
from .models import EventType
from .repository import EventTypeRepository


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
@events.route('/financial-delete/<int:event_id>', methods=['GET', 'POST'])
@login_required
@requires_roles('volunteer')
def delete_financial_event(event_id: int):
    if request.method == 'GET':
        return "delete form"
    elif request.method == 'POST':
        return "deleted!"


@events.route('/financial-edit/<int:event_id>', methods=['GET', 'POST'])
@login_required
@requires_roles('volunteer')
def edit_financial_event(event_id: int):
    if request.method == 'GET':
        return "edit form" + str(event_id)
    elif request.method == 'POST':
        return "updated!"


@events.route('/financial', methods=['GET', 'POST'])
@login_required
@requires_roles('volunteer')
def new_financial_event():
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


@events.route('/types', methods=['GET'])
@login_required
@requires_roles('volunteer')
def event_type_list():
    ev = EventTypeRepository.get_all_event_types()
    return render_template('eventtype/list.html', event_types=ev)


@events.route('/types/add', methods=['GET', 'POST'])
@login_required
@requires_roles('volunteer')
def event_type_add():
    form = EventTypeForm()
    if form.validate_on_submit():
        eventtype = EventType()
        eventtype.type_name = form.type_name.data
        eventtype.is_significant = form.is_significant.data
        EventTypeRepository.add_new_event_type(eventtype)
        return redirect(url_for('.event_type_list'))
    return render_template('eventtype/edit.html', form=form, title='Add')


@events.route('/types/edit/<et_id>', methods=['GET', 'POST'])
@login_required
@requires_roles('volunteer')
def event_type_edit(et_id):
    try:
        etype = EventTypeRepository.get_event_type_by_id(et_id)
    except NoResultFound:
        abort(404)
        return
    form = EventTypeForm()
    if form.validate_on_submit():
        etype.type_name = form.type_name.data
        etype.is_significant = form.is_significant.data
        EventTypeRepository.update_event_type(etype)
        return redirect(url_for('.event_type_list'))
    form = EventTypeForm(type_name=etype.type_name, is_significant=etype.is_significant)
    return render_template('eventtype/edit.html', form=form, title='Edit')


@events.route('/types/delete/<et_id>', methods=['GET', 'POST'])
@login_required
@requires_roles('volunteer')
def event_type_delete(et_id):
    try:
        etype = EventTypeRepository.get_event_type_by_id(et_id)
    except NoResultFound:
        abort(404)
        return
    free_type = EventTypeRepository.is_event_type_free(et_id)
    if request.method == 'POST':
        if free_type:
            EventTypeRepository.delete_event_type(et_id)
        return redirect(url_for('.event_type_list'))
    return render_template('eventtype/delete.html', name=etype.type_name,
                           free_type=free_type)
