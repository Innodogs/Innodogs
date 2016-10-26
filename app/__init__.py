import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

__author__ = 'Xomak'

db = SQLAlchemy()


def create_app(config_name):
    """Create an application instance."""
    app = Flask(__name__)
    cfg = os.path.join(os.getcwd(), 'config', config_name + '.py')
    app.config.from_pyfile(cfg)

    db.init_app(app)

    # Register blueprints

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .addrequests import add_requests as add_requests_blueprint
    app.register_blueprint(add_requests_blueprint, url_prefix='/add-requests')

    return app
