from flask import render_template, request, redirect
from flask_login import current_user
from datetime import datetime

from app.dogs.repository import DogsRepository
from . import dogs

__author__ = 'Xomak'


@dogs.route('/', methods=['GET', 'POST'])
def requests_list():
    all_dogs = DogsRepository.get_all_dogs()
    return render_template('dogs/list.html', dogs=all_dogs)

@dogs.route('/add', methods=['GET','POST'])
def requests_add():
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
    return render_template('dogs/add.html', date=datetime.now())

@dogs.route('/page/<int:dog_id>', methods=['GET','POST'])
def requests_page(dog_id):
    dog_data = DogsRepository.get_dog_by_id(dog_id)
    return render_template('dogs/page.html', dog=dog_data)
