"""
Events managment
"""

from flask import Blueprint

__author__ = 'Xomak'

event_type = Blueprint('eventtype', __name__, template_folder='templates', )

from . import routes
