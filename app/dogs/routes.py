from datetime import datetime

from flask import abort
from flask import render_template, url_for, redirect

from app import google_login
from . import dogs
from .repository import DogsRepository
from .models import Dog
from app.addrequests.forms import ApproveRequestForm
from app.addrequests.utils import convert_locations_to_select_choices
from app.locations.repository import LocationsRepository

__author__ = 'Xomak'


@dogs.route('/', methods=['GET', 'POST'])
def dogs_list():
    all_dogs = DogsRepository.get_all_dogs()
    return render_template('dogs/list.html', dogs=all_dogs, authorization_url=google_login.authorization_url())


@dogs.route('/<int:dog_id>', methods=['GET'])
def page_about_dog(dog_id):
    dog_data = DogsRepository.get_dog_by_id_with_events(dog_id)
    if dog_data is None:
        abort(404)
    return render_template('dogs/page.html', dog=dog_data)

@dogs.route('/add', methods=['GET','POST'])
def add_dog_without_request():
    add_dog_form = ApproveRequestForm()
    locations = LocationsRepository.get_all_locations()
    add_dog_form.location.choices = convert_locations_to_select_choices(locations)
    if add_dog_form.validate_on_submit():
        dog = Dog()
        dog.name = add_dog_form.name.data
        dog.sex = add_dog_form.sex.data
        dog.description = add_dog_form.description.data
        dog.is_hidden = add_dog_form.is_hidden.data
        dog.is_adopted = add_dog_form.is_adopted.data
        DogsRepository.new_dog(dog)
        return redirect(url_for('.dogs_list'))
    return render_template('dogs/add-new.html', date=datetime.now(), add_dog_form=add_dog_form)

