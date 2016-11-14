from flask import abort
from flask import render_template

from . import dogs
from .repository import DogsRepository

__author__ = 'Xomak'


@dogs.route('/', methods=['GET', 'POST'])
def dogs_list():
    all_dogs = DogsRepository.get_all_dogs()
    return render_template('dogs/list.html', dogs=all_dogs)


@dogs.route('/<int:dog_id>', methods=['GET'])
def page_about_dog(dog_id):
    dog_data = DogsRepository.get_dog_by_id_with_events(dog_id)
    if dog_data is None:
        abort(404)
    return render_template('dogs/page.html', dog=dog_data)
