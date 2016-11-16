from flask import redirect
from flask import url_for

from . import main

__author__ = 'Xomak'


@main.route('/', methods=['GET', 'POST'])
def index():
    return redirect(url_for('dogs.dogs_list'), code=301)
