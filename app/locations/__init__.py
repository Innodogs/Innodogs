"""
Adding and managing locations
"""

from flask import Blueprint

__author__ = 'Xomak'

locations = Blueprint('locations', __name__, template_folder='templates')

from . import routes
