from flask import session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user

from flask_app.models import User

class CreatePostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(min=5, max=100)])

    text = TextAreaField("Text")

    submit = SubmitField("Submit Post!")
    
class EmailForm(FlaskForm):
    email = StringField('Recipient Email:', validators=[DataRequired(), Email()])
    submit = SubmitField("Email Post")
