import os

from flask import Flask
from flask_login import LoginManager
from flask_oauth2_login import GoogleLogin
from flask_sqlalchemy import SQLAlchemy

__author__ = 'Xomak'

db = SQLAlchemy()
google_login = GoogleLogin()
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.session_protection = "strong"


def create_app(config_name):
    """Create an application instance."""
    app = Flask(__name__)
    cfg = os.path.join(os.getcwd(), 'config', config_name + '.py')
    app.config.from_pyfile(cfg)
    loaded = app.config.from_envvar('LOCAL_CONFIG', silent=True)
    if loaded:
        print(' * Local config is loaded')

    db.init_app(app)
    google_login.init_app(app)
    login_manager.init_app(app)
    # Register blueprints

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .addrequests import add_requests as add_requests_blueprint
    app.register_blueprint(add_requests_blueprint, url_prefix='/add-requests')

    from .dogs import dogs as dogs_blueprint
    app.register_blueprint(dogs_blueprint, url_prefix='/dogs')

    from .users import users as user_blueprint
    app.register_blueprint(user_blueprint, url_prefix='/users')

    return app
