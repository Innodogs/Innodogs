from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import TextAreaField
from wtforms.validators import DataRequired, Length


class AddRequestForm(FlaskForm):
    description = TextAreaField('Description', description='Description of a dog. Sex, possible location, etc.', validators=[
        DataRequired(),
        Length(min=4)
    ])
    pictures = FileField('Pictures', description='Pictures of a dog', validators=[
        FileAllowed(['jpg', 'png'], 'Images only!')
    ])


class RejectRequestForm(FlaskForm):
    comment = TextAreaField('Comment', validators=[DataRequired()])
