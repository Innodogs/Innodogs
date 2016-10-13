"""
Main application (contains main page and so on)
"""

from flask import Blueprint

__author__ = 'Xomak'

main = Blueprint('main', __name__, template_folder='templates')

from . import routes
