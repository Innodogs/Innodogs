from flask import abort
from flask import render_template, request, redirect
from datetime import datetime

from app.dogs.repository import DogsRepository
from app.addrequests.repository import AddRequestsRepository
from . import dogs

__author__ = 'Xomak'


@dogs.route('/', methods=['GET', 'POST'])
def requests_list():
    all_dogs = DogsRepository.get_all_dogs()
    return render_template('dogs/list.html', dogs=all_dogs)

@dogs.route('/approve-request/<req_id>', methods=['GET','POST'])
def requests_add(req_id):
    if request.method == 'POST':
        dog = Dog()
        dog.name = request.form['name']
        dog.sex = request.form['sex']
        dog.description = request.form['comment']
        dog.is_hidden = false
        dog.is_adopted = false
        DogsRepository.new_dog(dog)
        #abort(401)
        return redirect('/dogs')
    req = AddRequestsRepository.get_add_request_by_id(req_id)
    return render_template('dogs/add.html', date=datetime.now(), req=req)


@dogs.route('/<int:dog_id>', methods=['GET'])
def page_about_dog(dog_id):
    dog_data = DogsRepository.get_dog_by_id_with_events(dog_id)
    if dog_data is None:
        abort(404)
    return render_template('dogs/page.html', dog=dog_data)
