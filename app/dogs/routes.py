from flask import render_template

from app.dogs.repository import DogsRepository
from . import dogs

__author__ = 'Xomak'


@dogs.route('/', methods=['GET', 'POST'])
def requests_list():
    all_dogs = DogsRepository.get_all_dogs()
    return render_template('dogs/list.html', dogs=all_dogs)
