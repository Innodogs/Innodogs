from flask import render_template

from app.addrequests import add_requests
from app.addrequests.repository import AddRequestsRepository

__author__ = 'Xomak'


@add_requests.route('/', methods=['GET', 'POST'])
def requests_list():
    r = AddRequestsRepository.get_all_add_requests()
    return render_template('list.html', add_requests=r)


@add_requests.route('/add', methods=['GET', 'POST'])
def add_request():
    return render_template('add.html')
