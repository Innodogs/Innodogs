from flask import url_for, redirect, abort
from flask import render_template, request
from flask_login import login_required

from sqlalchemy.orm.exc import NoResultFound

from app.users.utils import requires_roles
from . import locations
from .models import Location
from .repository import LocationsRepository
from .forms import LocationsForm


@locations.route('/', methods=['GET'])
def locations_list():
    loc = LocationsRepository.get_all_locations()
    return render_template('locations/list.html', location_list = loc)

@locations.route('/add', methods=['GET','POST'])
@login_required
@requires_roles('volunteer')
def locations_add():
    form = LocationsForm()
    form.parent_id.choices = get_locations_id()
    if form.validate_on_submit():
        newlocation = Location()
        newlocation.name = form.name.data
        newlocation.description = form.description.data
        newlocation.parent_id = form.parent_id.data
        LocationsRepository.add_new_location(newlocation)
        return redirect(url_for('.locations_list'))
    return render_template('locations/edit.html', form=form, title='Add')

@locations.route('/<int:loc_id>/edit', methods=['GET','POST'])
@login_required
@requires_roles('volunteer')
def locations_edit(loc_id: int):
    try:
        loc = LocationsRepository.get_location_by_id(loc_id)
    except NoResultFound:
        abort(404)
        return
    form = LocationsForm(obj=loc, current_id=loc_id)
    form.parent_id.choices = get_locations_id()
    if form.validate_on_submit():
        loc.name = form.name.data
        loc.description = form.description.data
        loc.parent_id = form.parent_id.data
        LocationsRepository.update_location(loc)
        return redirect(url_for('.locations_list'))
    return render_template('locations/edit.html', form=form, title='Edit')

@locations.route('/<int:loc_id>/delete', methods=['GET','POST'])
@login_required
@requires_roles('volunteer')
def locations_delete(loc_id: int):
    try:
        loc = LocationsRepository.get_location_by_id(loc_id)
    except NoResultFound:
        abort(404)
        return
    free_location = LocationsRepository.is_location_free(loc_id)
    if request.method == 'POST':
        if free_location:
            LocationsRepository.delete_location(loc_id)
        return redirect(url_for('.locations_list'))
    return render_template('locations/delete.html', name=loc.name, free_location=True)

def get_locations_id():
    location = LocationsRepository.get_all_locations()
    return [(loc.id, loc.name) for loc in location]
