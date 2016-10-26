from flask import render_template

from app.addrequests import add_requests
from app.addrequests.repository import AddRequestsRepository

__author__ = 'Xomak'


@add_requests.route('/', methods=['GET', 'POST'])
def requests_list():
    r = AddRequestsRepository.get_all_add_requests()
    return render_template('addrequests/list.html', add_requests=r)

