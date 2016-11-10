#!/usr/bin/env python

"""
Runs the flask application
"""

import os

import psycopg2

from app import create_app

__author__ = 'Xomak'
dump_order = ["innodogs_public_add_request.sql",
              "innodogs_public_expenditure.sql",
              "innodogs_public_adoption_request.sql",
              "innodogs_public_comment.sql",
              "innodogs_public_location.sql",
              "innodogs_public_dog.sql",
              "innodogs_public_dog_picture.sql",
              "innodogs_public_event_type.sql",
              "innodogs_public_event.sql",
              "innodogs_public_inpayment.sql",
              "innodogs_public_user.sql"]


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
    for dump_file in dump_order:
        with open(os.path.join(_app.root_path, '../dump/{}'.format(dump_file)), mode='r', encoding='utf-8') as f:
            read = f.read()
            if read:
                connection.cursor().execute(read)
    connection.commit()
    print(' * Database has been successfully recreated')


if __name__ == '__main__':
    config_name = os.environ.get('FLASK_CONFIG') or 'development'
    print(' * Loading configuration "{0}"'.format(config_name))
    app = create_app(config_name)
    drop_create_db(app)
    app.run()
