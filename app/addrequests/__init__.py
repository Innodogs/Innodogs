"""
Add requests application (adding and managing add-requests)
"""

from flask import Blueprint

__author__ = 'Xomak'

add_requests = Blueprint('addrequests', __name__, template_folder='templates', )

from . import routes