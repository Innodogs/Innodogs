from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import TextAreaField, StringField, SelectField, BooleanField
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


class ApproveRequestForm(FlaskForm):
    name = StringField('Name', description='Name of the dog')
    sex = SelectField('Sex', choices=[('male', 'male'), ('female', 'female'), ('unknown', 'unknown')],
                      default='unknown', validators=[
            DataRequired()
        ])
    description = TextAreaField('Description', validators=[
        DataRequired(),
        Length(min=4)
    ], description='A comment about the dog')
    is_hidden = BooleanField('Is hidden', validators=[
        # DataRequired()
    ])
    is_adopted = BooleanField('Is adopted', validators=[
        # DataRequired()
    ])
    location = SelectField('Location', choices=[], coerce=int)
