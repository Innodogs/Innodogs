from flask import request

from . import events


@events.route('/edit/<int:event_id>', methods=['GET', 'POST'])
def edit_event(event_id: int):
    if request.method == 'GET':
        return "edit form" + str(event_id)
    elif request.method == 'POST':
        return "updated!"


@events.route('/', methods=['GET', 'POST'])
def new_event():
    if request.method == 'GET':
        return "new form"
    elif request.method == 'POST':
        return "added!"


# todo: исправить потом methods, после подключения javascript который будет пулять правильные методы для реквестов
@events.route('/delete/<int:event_id>', methods=['GET', 'POST'])
def delete_event(event_id: int):
    if request.method == 'GET':
        return "delete form"
    elif request.method == 'POST':
        return "deleted!"
