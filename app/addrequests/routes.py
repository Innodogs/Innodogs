import os
from datetime import datetime

import sqlalchemy.orm.exc
from flask import flash, url_for
from flask import redirect, request, abort
from flask import render_template
from flask_login import login_required

from app.dogs.forms import DogForm
from app.dogs.models import Dog, DogPicture
from app.dogs.repository import DogsRepository, DogPictureRepository
from app.users.utils import requires_roles
from app.utils.helpers import save_pictures
from . import add_requests
from .forms import AddRequestForm, RejectRequestForm
from .repository import AddRequestsRepository
from .utils import add_request_form_to_domain

__author__ = 'Xomak'


@add_requests.route('/', methods=['GET'])
@login_required
@requires_roles('volunteer')
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


@add_requests.route('/add', methods=['GET', 'POST'])
@login_required
def submit_add_request_form():
    form = AddRequestForm()
    if form.validate_on_submit():
        saved = AddRequestsRepository.save_add_request(add_request_form_to_domain(form))
        for abspath_image_file, relpath_image_file in save_pictures(request):
            is_saved = DogPictureRepository.insert_picture(
                DogPicture(request_id=saved.id, uri=relpath_image_file, is_main=False))
            if not is_saved:
                os.remove(abspath_image_file)

        flash('Thank you for your submission', 'info')
        return redirect(url_for('main.index'))
    return render_template('addrequests/add-request-form.html', form=form)


@add_requests.route('/<int:req_id>/approve', methods=['GET', 'POST'])
@login_required
@requires_roles('volunteer')
def add_dog_by_approving_request(req_id: int):
    form = DogForm()

    if form.validate_on_submit():
        dog = Dog()
        form.populate_obj(dog)
        saved = DogsRepository.new_dog(dog)

        req = AddRequestsRepository.get_add_request_by_id(req_id)

        pictures = DogPictureRepository.get_pictures_by_request_id(req_id)
        for pic in pictures:
            pic.is_main = pic.id == form.get_main_picture_id
            pic.dog_id = saved.id if pic.id not in form.get_list_of_deleted_picture_ids else None
            DogPictureRepository.update_picture(pic)

        req.status = 'approved'
        AddRequestsRepository.update_add_request(req)  # its not efficient, but it is effective. Do not change that
        return redirect(url_for('.requests_list'))
    req = AddRequestsRepository.get_add_request_by_id(req_id)
    pictures = DogPictureRepository.get_pictures_by_request_id(req_id)
    if pictures:
        form.main_picture_id.data = next(iter(pictures)).id
    return render_template('addrequests/approve.html', date=datetime.now(), req=req, pictures=pictures,
                           form=form)
