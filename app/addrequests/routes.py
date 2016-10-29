from flask import flash, redirect, url_for
from flask import render_template

from app.addrequests import add_requests
from app.addrequests.forms import AddRequestForm
from app.addrequests.repository import AddRequestsRepository
from werkzeug.utils import secure_filename

UPLOADS_FOLDER = '../uploads/'

__author__ = 'Xomak'


@add_requests.route('/', methods=['GET', 'POST'])
def requests_list():
    r = AddRequestsRepository.get_all_add_requests()
    return render_template('addrequests/list.html', add_requests=r)


@add_requests.route('/add-request-form/', methods=('GET', 'POST'))
def add_request_form():
    form = AddRequestForm()
    if form.validate_on_submit():
        filename = secure_filename(form.pictures.data.filename)
        form.pictures.data.save(UPLOADS_FOLDER + filename)
        flash('Thank you for your submission', 'info')
        return redirect(url_for('main.index'))
    return render_template('addrequests/add-request-form.html', form=form)
