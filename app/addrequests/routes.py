from flask import render_template, redirect, request, abort
from flask_login import login_required

import sqlalchemy.orm.exc

from app.addrequests import add_requests
from app.addrequests.repository import AddRequestsRepository
from app.users.utils import requires_roles

from datetime import datetime

__author__ = 'Xomak'


@add_requests.route('/', methods=['GET', 'POST'])
def requests_list():
    r = AddRequestsRepository.get_all_add_requests()
    return render_template('addrequests/list.html', add_requests=r)

@add_requests.route('/reject/<req_id>')
@login_required
@requires_roles('volunteer')
def requests_reject(req_id):
    try:
        req = AddRequestsRepository.get_add_request_by_id(req_id)
    except sqlalchemy.orm.exc.NoResultFound:
        abort(404)
    return render_template('addrequests/reject.html', req_id=req_id)

@add_requests.route('/reject/<req_id>/done', methods=['GET','POST'])
@login_required
@requires_roles('volunteer')
def requests_reject_finish(req_id):
    try:
        req = AddRequestsRepository.get_add_request_by_id(req_id)
        req.status = 'rejected'
        req.comment = request.form['comment']
        AddRequestsRepository.update_add_request(req)
    except sqlalchemy.orm.exc.NoResultFound:
        abort(404)
    return redirect('/add-requests/')

