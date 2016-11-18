from flask import redirect
from flask import render_template

from app import google_login
from app.dogs.repository import DogsRepository
from . import main

__author__ = 'Xomak'


@main.route('/', methods=['GET', 'POST'])
def index():
    return redirect("/dogs", code=302)
