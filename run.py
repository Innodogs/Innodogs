#!/usr/bin/env python

"""
Runs the flask application
"""

import os

import psycopg2

from app import create_app

__author__ = 'Xomak'


def drop_create_db(_app):
    def connect_db():
        """Connects to the database."""
        rv = psycopg2.connect(_app.config['SQLALCHEMY_DATABASE_URI'])
        return rv

    connection = connect_db()
    with _app.open_resource('../drop_db.sql', mode='r') as f:
        connection.cursor().execute(f.read())
    with _app.open_resource('../create_db.sql', mode='r') as f:
        connection.cursor().execute(f.read())
    connection.commit()
    print(' * Database has been successfully recreated')


if __name__ == '__main__':
    config_name = os.environ.get('FLASK_CONFIG') or 'development'
    print(' * Loading configuration "{0}"'.format(config_name))
    app = create_app(config_name)
    drop_create_db(app)
    app.run()
