import os
from datetime import datetime

import sqlalchemy.orm.exc
from flask import flash, url_for
from flask import redirect, request, abort
from flask import render_template, current_app
from flask_login import login_required
from werkzeug.utils import secure_filename

from app.dogs.models import Dog
from app.dogs.repository import DogsRepository
from app.locations.repository import LocationsRepository
from app.users.utils import requires_roles
from . import add_requests
from .forms import AddRequestForm, RejectRequestForm, ApproveRequestForm
from .repository import AddRequestsRepository
from .utils import add_request_form_to_domain, convert_locations_to_select_choices

__author__ = 'Xomak'


@add_requests.route('/', methods=['GET'])
@login_required
def requests_list():
    r = AddRequestsRepository.get_all_add_requests()
    return render_template('addrequests/list.html', add_requests=r)


@add_requests.route('/reject/<int:req_id>', methods=['GET', 'POST'])
@login_required
@requires_roles('volunteer')
def requests_reject(req_id: int):
    try:
        req = AddRequestsRepository.get_add_request_by_id(req_id)
    except sqlalchemy.orm.exc.NoResultFound:
        abort(404)
        return

    form = RejectRequestForm()
    if form.validate_on_submit():
        req.status = 'rejected'
        req.comment = request.form['comment']
        AddRequestsRepository.update_add_request(req)
        return redirect(url_for('.requests_list'))
    return render_template('addrequests/reject.html', req_id=req_id, form=form)


@add_requests.route('/', methods=['POST'])
@login_required
def submit_add_request_form():
    form = AddRequestForm()
    if form.validate_on_submit():
        filename = secure_filename(form.pictures.data.filename)
        if form.pictures.data.filename != '':
            form.pictures.data.save(
                os.path.join(current_app.config['UPLOAD_FOLDER'], filename))  # current_app -> probably fine
        AddRequestsRepository.save_add_request(add_request_form_to_domain(form))
        flash('Thank you for your submission', 'info')
        return redirect(url_for('main.index'))
    return render_template('addrequests/add-request-form.html', form=form)


@add_requests.route('/add', methods=['GET'])
@login_required
def add_request_form():
    form = AddRequestForm()
    return render_template('addrequests/add-request-form.html', form=form)


@add_requests.route('/approve/<int:req_id>', methods=['GET', 'POST'])
def add_dog_by_approving_request(req_id: int):
    approve_request_form = ApproveRequestForm()
    locations = LocationsRepository.get_all_locations()
    approve_request_form.location.choices = convert_locations_to_select_choices(locations)

    if approve_request_form.validate_on_submit():
        dog = Dog()
        dog.name = approve_request_form.name.data
        dog.sex = approve_request_form.sex.data
        dog.description = approve_request_form.description.data
        dog.is_hidden = approve_request_form.is_hidden.data
        dog.is_adopted = approve_request_form.is_adopted.data
        dog.location_id = approve_request_form.location.data
        DogsRepository.new_dog(dog)
        return redirect(url_for('.requests_list'))
    req = AddRequestsRepository.get_add_request_by_id(req_id)
    return render_template('addrequests/approve.html', date=datetime.now(), req=req,
                           approve_request_form=approve_request_form)
