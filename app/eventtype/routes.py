
from flask import render_template
from flask import redirect, request, url_for

import sqlalchemy.orm.exc

from app.eventtype import event_type
from app.eventtype.repository import EventTypeRepository
from app.eventtype.forms import EventTypeForm
from app.eventtype.models import EventType

__author__ = 'Xomak'

@event_type.route('/', methods=['GET'])
#@login_required
def event_type_list():
    ev = EventTypeRepository.get_all_event_types()
    return render_template('eventtype/list.html', event_types=ev)

@event_type.route('/add', methods=['GET','POST'])
def event_type_add():
    form = EventTypeForm()
    if form.validate_on_submit():
        eventtype = EventType()        
        eventtype.type_name = form.type_name.data
        eventtype.is_significant = form.is_significant.data
        EventTypeRepository.add_new_event_type(eventtype)
        return redirect('/events/')
    return render_template('eventtype/edit.html', form=form, title='Add')
    
@event_type.route('/edit/<et_id>', methods=['GET','POST'])
def event_type_edit(et_id):
    try:
        etype = EventTypeRepository.get_event_type_by_id(et_id)
    except sqlalchemy.orm.exc.NoResultFound:
        abort(404)
    form = EventTypeForm() 
    if form.validate_on_submit():
        etype.type_name = form.type_name.data
        etype.is_significant = form.is_significant.data
        EventTypeRepository.update_event_type(etype)
        return redirect('/events/')   
    form = EventTypeForm(type_name=etype.type_name, is_significant=etype.is_significant)
    return render_template('eventtype/edit.html', form=form, title='Edit')
    
@event_type.route('/delete/<et_id>', methods=['GET','POST'])
def event_type_delete(et_id):
    try:
        etype = EventTypeRepository.get_event_type_by_id(et_id)
    except sqlalchemy.orm.exc.NoResultFound:
        abort(404)
    if request.method == 'POST':
       EventTypeRepository.delete_event_type(et_id)
       return redirect('/events/')
    return render_template('eventtype/delete.html', name=etype.type_name)
    

