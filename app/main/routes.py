from flask import render_template, jsonify

from app import google_login
from . import main

__author__ = 'Xomak'


@main.route('/', methods=['GET', 'POST'])
@main.route('/login/google', methods=['GET', 'POST'])
def main():
    return render_template('main.html', authorization_url=google_login.authorization_url())


@google_login.login_success
def login_success(token, profile):
    return jsonify(token=token, profile=profile)


@google_login.login_failure
def login_failure(e):
    return jsonify(error=str(e))
