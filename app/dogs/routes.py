import os
import re
from datetime import datetime

import flask
from flask import abort, jsonify
from flask import current_app
from flask import flash
from flask import render_template, url_for, redirect
from flask import request
from flask_login import login_required
from wtforms import BooleanField

from app.dogs.forms import DogForm
from app.dogs.forms import DogsFilterForm
from app.events.repository import EventTypeRepository
from app.users.utils import requires_roles
from app.utils.helpers import save_pictures
from app.utils.pages_helper import Pages
from . import dogs
from .models import Dog, DogPicture
from .repository import DogsRepository, DogPictureRepository

__author__ = 'Xomak'


@dogs.route('/', methods=['GET'])
def dogs_list():
    event_types_ids = []
    filter_args = {}
    page_number = 1

    significant_event_regexp = re.compile(r"^event_(\d+)$")
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
            if (key == 'location_id') and value is not None and value >= 0:
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

    dogs_number = DogsRepository.get_dogs_count_satisfying_criteria(**filter_args)
    try:
        pages = Pages('.dogs_list', current_app.config['DOGS_PER_PAGE'], page_number, dogs_number, request.args)
    except ValueError:
        abort(404)

    all_dogs = DogsRepository.get_dogs_with_significant_events_by_criteria(**filter_args,
                                                                           from_row=pages.get_start_row(),
                                                                           rows_count=pages.get_rows_number())
    for dog in all_dogs:
        distinct_events_list = set()
        for event in dog.events:
            if event.event_type.type_name in distinct_events_list:
                dog.events.remove(event)
            else:
                distinct_events_list.add(event.event_type.type_name)

    return render_template('dogs/list.html', dogs_with_events=all_dogs, filter_form=filter_form, pages=pages)


@dogs.route('/<int:dog_id>', methods=['GET'])
def page_about_dog(dog_id: int):
    dog = DogsRepository.get_dog_by_id_and_pics_and_events_and_location(dog_id)
    if dog is None:
        abort(404)
    return render_template('dogs/page.html', dog=dog)


@dogs.route('/json/dogs-by-keyword')
def json_search_dogs():
    term = request.args.get('term')
    result = []
    if term is not None and len(term) > 2:
        dogs_list = DogsRepository.get_dogs_by_name_part(term)
        for dog in dogs_list:
            current_record = dict()
            current_record['id'] = dog.id
            current_record['text'] = str("{} ({})").format(dog.name, dog.id)
            result.append(current_record)
    return flask.jsonify(result)


@dogs.route('/add', methods=['GET', 'POST'])
@login_required
@requires_roles('volunteer')
def add_dog_without_request():
    add_dog_form = DogForm()
    if add_dog_form.validate_on_submit():
        dog = Dog()
        add_dog_form.populate_obj(dog)
        saved_dog = DogsRepository.new_dog(dog)
        for i, (abspath_image_file, relpath_image_file) in enumerate(save_pictures(request)):
            is_first = i == 0
            picture = DogPicture(dog_id=saved_dog.id, uri=relpath_image_file, is_main=is_first)
            is_saved = DogPictureRepository.insert_picture(picture)
            if not is_saved:
                os.remove(abspath_image_file)

        flash("Added a dog with name {}".format(dog.name) if dog.name else "Added a dog with id {}".format(dog.id))
        return redirect(url_for('.dogs_list'))
    return render_template('dogs/add-new.html', date=datetime.now(), add_dog_form=add_dog_form)


@dogs.route('/<int:dog_id>/edit', methods=['POST', 'GET'])
@login_required
@requires_roles('volunteer')
def edit(dog_id: int):
    if request.method == 'GET':
        dog = DogsRepository.get_dog_by_id_with_pictures(dog_id)
        form = DogForm(obj=dog)
        form.main_picture_id.data = dog.main_picture.id if dog.main_picture else None
        return render_template('dogs/edit.html', form=form, dog=dog)

    form = DogForm()
    if form.validate_on_submit():
        dog = Dog()
        form.populate_obj(dog)
        DogsRepository.update_dog(dog)
        return redirect(url_for('.page_about_dog', dog_id=dog_id))
    dog = DogsRepository.get_dog_by_id_with_pictures(dog_id)
    form = DogForm(obj=dog)
    form.main_picture_id.data = dog.main_picture.id if dog.main_picture else None
    return render_template('dogs/edit.html', form=form, dog=dog)
