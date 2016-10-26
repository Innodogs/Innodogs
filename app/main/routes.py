from flask import render_template

from app import google_login
from . import main

__author__ = 'Xomak'


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('main.html', authorization_url=google_login.authorization_url())
