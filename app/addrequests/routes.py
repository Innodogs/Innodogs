import os
import uuid
from datetime import datetime

import sqlalchemy.orm.exc
from flask import flash, url_for
from flask import redirect, request, abort
from flask import render_template, current_app
from flask_login import login_required
from werkzeug.utils import secure_filename

from app.dogs.models import Dog, DogPicture
from app.dogs.repository import DogsRepository, DogPictureRepository
from app.users.utils import requires_roles
from . import add_requests
from .forms import AddRequestForm, RejectRequestForm, ApproveRequestForm
from .repository import AddRequestsRepository
from .utils import add_request_form_to_domain

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


@add_requests.route('/add', methods=['GET', 'POST'])
@login_required
def submit_add_request_form():
    form = AddRequestForm()
    if form.validate_on_submit():
        saved = AddRequestsRepository.save_add_request(add_request_form_to_domain(form))
        images = request.files.getlist('pictures')
        if images:
            for img in images:
                # Create Images
                file_name = str(uuid.uuid4()) + secure_filename(img.filename)
                abspath_image_file = os.path.join(current_app.config['UPLOAD_FOLDER_ABSOLUTE'], file_name)
                relpath_image_file = os.path.join(current_app.config['UPLOAD_FOLDER'], file_name)
                img.save(abspath_image_file)

                # Save record
                is_saved = DogPictureRepository.insert_picture(
                    DogPicture(request_id=saved.id, uri=relpath_image_file, is_main=False))
                if not is_saved:
                    os.remove(abspath_image_file)

        flash('Thank you for your submission', 'info')
        return redirect(url_for('main.index'))
    return render_template('addrequests/add-request-form.html', form=form)


@add_requests.route('/<int:req_id>/approve', methods=['GET', 'POST'])
def add_dog_by_approving_request(req_id: int):
    approve_request_form = ApproveRequestForm()
    if approve_request_form.validate_on_submit():
        dog = Dog()
        approve_request_form.populate_obj(dog)
        DogsRepository.new_dog(dog)

        req = AddRequestsRepository.get_add_request_by_id(req_id)
        req.status = 'approved'
        AddRequestsRepository.update_add_request(req)  # its not efficient, but it is effective. Do not change that
        return redirect(url_for('.requests_list'))
    req = AddRequestsRepository.get_add_request_by_id(req_id)
    pictures = DogPictureRepository.get_pictures_by_request_id(req_id)
    return render_template('addrequests/approve.html', date=datetime.now(), req=req, pictures=pictures,
                           approve_request_form=approve_request_form)
