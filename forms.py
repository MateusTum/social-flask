from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, DateField
from wtforms.validators import DataRequired, URL, Length, EqualTo
from flask_ckeditor import CKEditorField


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")


class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(),
                                                     Length(min=8, max=16),
                                                     EqualTo('password_confirm',
                                                             message='Passwords must match')])
    password_confirm = PasswordField("Repeat Password", validators=[DataRequired(), Length(min=8, max=16)])
    submit = SubmitField("Register")
