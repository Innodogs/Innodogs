import os

from flask import Flask
from flask_login import LoginManager
from flask_oauth2_login import GoogleLogin
from flask_sqlalchemy import SQLAlchemy

__author__ = 'Xomak'

db = SQLAlchemy()
google_login = GoogleLogin()
login_manager = LoginManager()
login_manager.login_view = "main.index"
login_manager.session_protection = "strong"


def create_app(config_name):
    """Create an application instance."""
    app = Flask(__name__)
    cfg = os.path.join(os.getcwd(), 'config', config_name + '.py')
    app.config.from_pyfile(cfg)
    loaded = app.config.from_envvar('LOCAL_CONFIG', silent=True)
    if loaded:
        app.config['UPLOAD_FOLDER_ABSOLUTE'] = os.path.join(app.static_folder, app.config['UPLOAD_FOLDER'])
        print(' * Local config is loaded:')
        print(' *   UPLOAD_FOLDER_ABSOLUTE=' + app.config['UPLOAD_FOLDER_ABSOLUTE'])
        print(' *   UPLOAD_FOLDER=' + app.config['UPLOAD_FOLDER'])

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

    from .events import events as events_blueprint
    app.register_blueprint(events_blueprint, url_prefix='/events')

    from .locations import locations as locations_blueprint
    app.register_blueprint(locations_blueprint, url_prefix='/locations')

    from .after_init import after_init
    after_init(app)

    return app
