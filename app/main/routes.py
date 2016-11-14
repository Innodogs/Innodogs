from flask import redirect
from flask import render_template

from app import google_login
from app.dogs.repository import DogsRepository
from . import main

__author__ = 'Xomak'


@main.route('/', methods=['GET', 'POST'])
def index():
    all_dogs = DogsRepository.get_all_dogs()
    return redirect("/dogs", code=302)
    #return render_template('dogs/list.html', dogs=all_dogs, authorization_url=google_login.authorization_url())
    #return render_template('base.html', authorization_url=google_login.authorization_url())

