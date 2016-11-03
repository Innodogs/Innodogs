from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import TextAreaField
from wtforms.validators import DataRequired, Length


class AddRequestForm(FlaskForm):
    description = TextAreaField('Description', validators=[
        DataRequired(),
        Length(min=4)
    ])
    pictures = FileField('Pictures', validators=[
        FileAllowed(['jpg', 'png'], 'Images only!')
    ])

class RejectRequestForm(FlaskForm):
    comment = TextAreaField('Comment', validators=[DataRequired()])
