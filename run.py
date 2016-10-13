#!/usr/bin/env python

"""
Runs the flask application
"""

import os
from app import create_app

__author__ = 'Xomak'

if __name__ == '__main__':
    config_name = os.environ.get('FLASK_CONFIG') or 'development'
    print(' * Loading configuration "{0}"'.format(config_name))
    app = create_app(config_name)
    app.run()