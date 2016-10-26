"""
Main application (contains main page and so on)
"""

from flask import Blueprint

__author__ = 'Xomak'

users = Blueprint('users', __name__, template_folder='templates')

from . import routes
from . import utils
