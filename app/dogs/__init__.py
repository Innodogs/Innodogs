"""
Dogs application (adding and managing add-requests)
"""

from flask import Blueprint

__author__ = 'Xomak'

dogs = Blueprint('dogs', __name__, template_folder='templates', )

from . import routes
