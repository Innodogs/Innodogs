import re
from datetime import datetime

import math
from flask import abort
from flask import render_template, url_for, redirect
from flask import request
from wtforms import BooleanField

from app.dogs.forms import DogsFilterForm
from app.events.repository import EventTypeRepository
from . import dogs
from flask import current_app
from .repository import DogsRepository
from .models import Dog
from app.addrequests.forms import ApproveRequestForm
from app.addrequests.utils import convert_locations_to_select_choices
from app.locations.repository import LocationsRepository

__author__ = 'Xomak'


@dogs.route('/', methods=['GET'])
def dogs_list():
    event_types_ids = []
    filter_args = {}
    significant_event_regexp = re.compile(r"^event_(\d+)$")
    page_number = 1

    significant_event_types = EventTypeRepository.get_significant_event_types()

    class FilterForm(DogsFilterForm):
        pass

    for event_type in significant_event_types:
        setattr(FilterForm, "event_%s" % event_type.id, BooleanField(event_type.type_name))

    filter_form = FilterForm(request.args, csrf_enabled=False)
    if filter_form.validate():
        for field in filter_form:
            key = field.name
            value = field.data

            if (key == 'sex' or key == 'name') and value is not None and len(value) > 0 and value != 'None':
                filter_args[key] = value

            if key == 'is_adopted' and value:
                filter_args[key] = True

            if key == 'page' and value is not None:
                page_number = value

            match_result = significant_event_regexp.match(key)
            if match_result and value:
                event_types_ids.append(match_result.group(1))

    if len(event_types_ids) > 0:
        filter_args['event_types_ids'] = event_types_ids


    rows_count = current_app.config['DOGS_PER_PAGE']
    dogs_number = DogsRepository.get_dogs_count_satisfying_criteria(**filter_args)
    current_start_row = (page_number-1)*current_app.config['DOGS_PER_PAGE']
    pages_number = math.ceil(dogs_number/rows_count)
    if current_start_row < 0 or current_start_row > dogs_number:
        abort(404)

    all_dogs = DogsRepository.get_dogs_with_significant_events_by_criteria(**filter_args, from_row=current_start_row, rows_count=rows_count)
    for dog in all_dogs:
        distinct_events_list = set()
        for event in dog.events:
            if event.event_type.type_name in distinct_events_list:
                dog.events.remove(event)
            else:
                distinct_events_list.add(event.event_type.type_name)

    pages_list = [1]
    for current_page in range(page_number-3, page_number+3):
        if 0 < current_page <= pages_number and current_page not in pages_list:
                pages_list.append(current_page)

    request_args = dict(request.args)
    if 'page' in request_args:
        del request_args['page']

    return render_template('dogs/list.html', dogs_with_events=all_dogs, filter_form=filter_form,
                           pages_number=pages_number, current_page=page_number, request_args=request_args, pages_list=pages_list)


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

