import os
from datetime import datetime

from flask import flash, url_for
from flask import redirect, request, abort
from flask import render_template, current_app
from flask_login import login_required
from werkzeug.utils import secure_filename

import sqlalchemy.orm.exc

from app.addrequests import add_requests
from app.addrequests.forms import AddRequestForm, RejectRequestForm
from app.addrequests.repository import AddRequestsRepository
from app.addrequests.utils import add_request_form_to_domain
from app.users.utils import requires_roles

__author__ = 'Xomak'


@add_requests.route('/', methods=['GET'])
@login_required
def requests_list():
    r = AddRequestsRepository.get_all_add_requests()
    return render_template('addrequests/list.html', add_requests=r)

@add_requests.route('/reject/<req_id>', methods=['GET','POST'])
@login_required
@requires_roles('volunteer')
def requests_reject(req_id):
    try:
        req = AddRequestsRepository.get_add_request_by_id(req_id)
    except sqlalchemy.orm.exc.NoResultFound:
        abort(404)
    form = RejectRequestForm()
    if form.validate_on_submit():
        req.status = 'rejected'
        req.comment = request.form['comment']
        AddRequestsRepository.update_add_request(req)
        return redirect('/add-requests/')
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


@add_requests.route('/add-form', methods=['GET'])
@login_required
def add_request_form():
    form = AddRequestForm()
    return render_template('addrequests/add-request-form.html', form=form)
