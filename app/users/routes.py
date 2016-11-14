from flask import flash
from flask import json, jsonify
from flask import redirect
from flask import render_template
from flask import session
from flask import url_for
from flask_login import login_required, login_user, logout_user

from app import google_login
from . import users
from .models import User
from .repository import UsersRepository
from .utils import requires_roles


@users.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    return render_template('profile.html')


# the order of the wrappers matters (!)
@users.route('/only_for_admin', methods=['GET'])
@login_required
@requires_roles('admin')
def only_for_admin():
    """Special section for admin. Only for test purposes. Could be removed."""
    return 'for admin only'


# user_info and token comes from google
@google_login.login_success
def login_success_callback(token, user_info):
    user_info['google_id'] = user_info.pop('id')  # rename id key to google_id
    user = User(**user_info)

    from_db = UsersRepository.get_user_by_google_id(user.google_id)
    if not from_db:
        from_db = UsersRepository.save_user(user)

    is_logged = login_user(from_db, remember=True)
    if is_logged:
        session['token'] = json.dumps(token)
        return redirect(url_for('users.profile'))
    else:
        flash('Cannot log in. You are inactive user. Please, contact your system administrator', 'info')
        return redirect(url_for('main.index'))


@users.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@google_login.login_failure
def login_failure_callback(e):
    return jsonify(error=str(e))


@users.route('/list')
def user_list():
    users = UsersRepository.get_all_users()
    return render_template('list.html', users=users)
