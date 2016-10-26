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
def login_success(token, userinfo):
    user = User(**userinfo)
    login_user(user)
    session['token'] = json.dumps(token)
    return redirect(url_for('users.profile'))


@google_login.login_failure
def login_failure(e):
    return jsonify(error=str(e))
