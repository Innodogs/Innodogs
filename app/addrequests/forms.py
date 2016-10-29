from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import TextAreaField
from wtforms.validators import DataRequired


class AddRequestForm(FlaskForm):
    description = TextAreaField('Description', validators=[
        DataRequired()
    ])
    pictures = FileField('Pictures', validators=[
        FileAllowed(['jpg', 'png'], 'Images only!')
    ])
