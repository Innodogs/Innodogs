from flask import json, jsonify
from flask import redirect
from flask import render_template
from flask import session
from flask import url_for
from flask_login import login_required, login_user

from app import google_login
from app.users.repository import UsersRepository
from . import users
from .models import User


@login_required
@users.route("/profile", methods=["GET", "POST"])
def profile():
    return render_template('profile.html')


@google_login.login_success
def login_success(token, user_info):
    user_info['google_id'] = user_info.pop('id')  # rename id key to google_id
    user = User(**user_info)

    from_db = UsersRepository.get_user_by_google_id(user.google_id)
    if not from_db:
        from_db = UsersRepository.save_user(user)

    login_user(from_db)
    session['token'] = json.dumps(token)
    return redirect(url_for('users.profile'))


@google_login.login_failure
def login_failure(e):
    return jsonify(error=str(e))
