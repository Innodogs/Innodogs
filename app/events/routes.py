from flask import abort, url_for
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask_login import login_required
from sqlalchemy.orm.exc import NoResultFound

from app.dogs.repository import DogsRepository
from app.users.utils import requires_roles
from . import events
from .finance.forms import InpaymentEventForm, FinantialEventsForm, ExpenditureForm
from .finance.models import Inpayment
from .finance.repository import InpaymentRepository, ExpenditureRepository
from .forms import EventTypeForm, EventForm, EventWithDogForm
from .models import EventType, Expenditure, Event
from .repository import EventTypeRepository, EventRepository


@events.route('/events/<int:event_id>/edit-with-dog', methods=['GET', 'POST'])
@login_required
@requires_roles('volunteer')
def edit_event_with_dog(event_id: int):
    try:
        event = EventRepository.get_event_by_id(event_id)
    except NoResultFound:
        abort(404)
    if event.expenditure_id is None:
        abort(404)
    associated_dog = DogsRepository.get_dog_by_id(event.dog_id)
    form = EventWithDogForm(obj=event)
    if form.validate_on_submit():
        form.populate_obj(event)
        EventRepository.update_event(event)
        return redirect(url_for('.edit_expenditure', expenditure_id=event.expenditure_id))
    else:
        return render_template('event/event_form_with_dog.html', action='.edit_event_with_dog', form=form,
                               expenditure_id=event.expenditure_id, dog_name=associated_dog.name, event_id=event_id)


@events.route('/add-for/expenditure/<int:expenditure_id>', methods=['GET', 'POST'])
@login_required
@requires_roles('volunteer')
def add_for_expenditure(expenditure_id: int):
    try:
        expenditure = ExpenditureRepository.get_expenditure_by_id(expenditure_id)
    except NoResultFound:
        abort(404)
    form = EventWithDogForm()
    if form.validate_on_submit():
        event = Event()
        event.expenditure_id = expenditure_id
        form.populate_obj(event)
        EventRepository.add_new_event(event)
        return redirect(url_for('.edit_expenditure', expenditure_id=expenditure_id))
    else:
        return render_template('event/event_form_with_dog.html', action='.add_for_expenditure', form=form,
                               expenditure_id=expenditure_id)


@events.route('/add-for/dog/<int:dog_id>', methods=['GET', 'POST'])
@login_required
@requires_roles('volunteer')
def add_for_dog(dog_id: int):
    try:
        dog = DogsRepository.get_dog_by_id(dog_id)
    except NoResultFound:
        abort(404)
    form = EventForm()
    if form.validate_on_submit():
        event = Event()
        event.dog_id = dog_id
        form.populate_obj(event)
        EventRepository.add_new_event(event)
        return redirect(url_for('dogs.page_about_dog', dog_id=dog_id))
    else:
        return render_template('event/event_form.html', action='.add_for_dog', form=form, dog_id=dog_id)


@events.route('/<int:event_id>/edit', methods=['GET', 'POST'])
@login_required
@requires_roles('volunteer')
def edit_event(event_id: int):
    try:
        event = EventRepository.get_event_by_id(event_id)
    except NoResultFound:
        abort(404)
    form = EventForm(obj=event)
    if form.validate_on_submit():
        form.populate_obj(event)
        EventRepository.update_event(event)
        return redirect(url_for('dogs.page_about_dog', dog_id=event.dog_id))
    else:
        return render_template('event/event_form.html', action='.edit_event', form=form, event_id=event_id)


@events.route('/financial/<int:event_id>/delete', methods=['GET', 'POST'])
@login_required
@requires_roles('volunteer')
def delete_financial_event(event_id: int):
    if request.method == 'GET':
        return "delete form"
    elif request.method == 'POST':
        return "deleted!"


@events.route('/financial/<int:event_id>/edit', methods=['GET', 'POST'])
@login_required
@requires_roles('volunteer')
def edit_financial_event(event_id: int):
    if request.method == 'GET':
        return "edit form" + str(event_id)
    elif request.method == 'POST':
        return "updated!"


@events.route('/financial/expenditure/add', methods=['GET', 'POST'])
@login_required
@requires_roles('volunteer')
def new_expenditure():
    form = ExpenditureForm()
    if form.validate_on_submit():
        expenditure = Expenditure()
        form.populate_obj(expenditure)
        ExpenditureRepository.add_new_expenditure(expenditure)
        return redirect(url_for('.edit_expenditure', expenditure_id=expenditure.id))
    else:
        return render_template('finance/expenditure_form.html', action='.new_expenditure', form=form)


@events.route('/financial/expenditure/<int:expenditure_id>/edit', methods=['GET', 'POST'])
@login_required
@requires_roles('volunteer')
def edit_expenditure(expenditure_id: int):
    try:
        expenditure = ExpenditureRepository.get_expenditure_by_id(expenditure_id)
    except NoResultFound:
        abort(404)

    related_events = EventRepository.get_events_by_expenditure_id(expenditure_id)
    form = ExpenditureForm(obj=expenditure)
    if form.validate_on_submit():
        form.populate_obj(expenditure)
        ExpenditureRepository.update_expenditure(expenditure)
        return redirect(url_for('.inpayments_list'))
    else:
        return render_template('finance/expenditure_form.html', action='.edit_expenditure', form=form, id=expenditure_id, related_events=related_events)


@events.route('/financial', methods=['GET', 'POST'])
@login_required
@requires_roles('volunteer')
def inpayments_list_date():
    form = FinantialEventsForm()
    startdate = form.startdatetime.data
    enddate = form.enddatetime.data
    inps = InpaymentRepository.get_all_inpayments()
    if (startdate is not None and enddate is not None):
        inps = InpaymentRepository.get_all_inpayments_by_date(startdate, enddate)
    return render_template('finance/list.html', inpayments=inps, form=form, action='.inpayments_list_date')



@events.route('/<int:event_id>/delete', methods=['GET', 'POST'])
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


@events.route('/types/<int:et_id>/edit', methods=['GET', 'POST'])
@login_required
@requires_roles('volunteer')
def event_type_edit(et_id: int):
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


@events.route('/types/<int:et_id>/delete', methods=['GET', 'POST'])
@login_required
@requires_roles('volunteer')
def event_type_delete(et_id: int):
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


@events.route('/inpayments/add', methods=['GET', 'POST'])
@login_required
@requires_roles('volunteer')
def add_inpayment():
    form = InpaymentEventForm()
    if form.validate_on_submit():
        inpayment = Inpayment()
        form.populate_obj(inpayment)
        InpaymentRepository.add_new_inpayment(inpayment)
        flash('Inpayment added!', 'info')
        return redirect(url_for('.add_inpayment'))
    return render_template('finance/inpayment_form.html', form=form, title='Add inpayment', action='.add_inpayment')


@events.route('/inpayments/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@requires_roles('volunteer')
def edit_inpayment(id: int):
    inpayment = InpaymentRepository.get_inpayment_by_id(id)
    form = InpaymentEventForm(obj=inpayment)
    if form.validate_on_submit():
        inpayment = Inpayment()
        form.populate_obj(inpayment)
        InpaymentRepository.update_inpayment(inpayment)
        flash('Inpayment updated!', 'info')
        return redirect(url_for('.edit_inpayment', id=inpayment.id))
    return render_template('finance/inpayment_form.html', form=form, title='Edit inpayment', action='.edit_inpayment',
                           id=inpayment.id)
