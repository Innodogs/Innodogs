from functools import wraps

from flask import abort
from flask import render_template
from flask_login import current_user

from app import login_manager
from app.users import users
from .repository import UsersRepository


@login_manager.user_loader
def load_user(google_id):
    if google_id is None:
        return None
    return UsersRepository.get_user_by_google_id(str(google_id))


@users.errorhandler(403)
def access_denied_response(e):
    """Example of access is denied response. Not final. Could be removed"""
    return render_template('access_denied_response.html'), 403


def requires_roles(*allowed_roles):
    """Wrapper for any function that requires some roles restrictions:

    :Example:

    @requires_roles('admin','admin2')
    def f():
        ...

    f is wrapped into requires_roles wrapper and f will be executed only if current_user has admin or admin2 roles.
    """

    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if any(role in allowed_roles for role in current_user.get_roles()):
                return f(*args, **kwargs)
            return abort(403)

        return wrapped

    return wrapper
