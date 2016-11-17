"""
Development configuration file
"""

DEBUG=True
SQLALCHEMY_DATABASE_URI=''
SQLALCHEMY_TRACK_MODIFICATIONS=False # This feature is not needed in our app, but default value raises warnings
DOGS_PER_PAGE=10
UPLOAD_FOLDER='dogs'