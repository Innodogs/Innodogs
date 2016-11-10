"""
Dogs application (adding and managing add-requests)
"""

from flask import Blueprint

__author__ = 'mputilov'

events = Blueprint('events', __name__, template_folder='templates', )

from . import routes
