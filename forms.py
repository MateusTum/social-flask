from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, DateField, TextAreaField
from wtforms.validators import DataRequired, URL, Length, EqualTo, Optional
from flask_ckeditor import CKEditorField


# Login form ----------------------------------------------------
class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")


# Register form ----------------------------------------------------
class RegisterForm(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(),
                                                     Length(min=8, max=16),
                                                     EqualTo('password_confirm',
                                                             message='Passwords must match')])
    password_confirm = PasswordField("Repeat Password", validators=[DataRequired(), Length(min=8, max=16)])
    submit = SubmitField("Register")


# Post form ----------------------------------------------------
class PostForm(FlaskForm):
    title = StringField("Post Title", validators=[DataRequired()])
    content = CKEditorField("Post Content", validators=[DataRequired()])
    submit = SubmitField("Post")


# Comment form ----------------------------------------------------
class CommentForm(FlaskForm):
    content = CKEditorField("Comment Content", validators=[DataRequired()])
    submit = SubmitField("Post")


# Profile Form ----------------------------------------------------
class UserProfileForm(FlaskForm):
    bio = TextAreaField('Bio', validators=[Optional(), Length(max=255)])
    phone_number = StringField('Phone Number', validators=[Optional(), Length(max=15)])
    date_of_birth = DateField('Date of Birth', format='%Y-%m-%d', validators=[Optional()])
    street_address = StringField('Street Address', validators=[Optional(), Length(max=255)])
    city = StringField('City', validators=[Optional(), Length(max=100)])
    state = StringField('State', validators=[Optional(), Length(max=100)])
    postal_code = StringField('Postal Code', validators=[Optional(), Length(max=20)])
    country = StringField('Country', validators=[Optional(), Length(max=100)])
    gender = StringField('Gender', validators=[Optional(), Length(max=10)])
    occupation = StringField('Occupation', validators=[Optional(), Length(max=100)])
    company = StringField('Company', validators=[Optional(), Length(max=100)])
    education = StringField('Education', validators=[Optional(), Length(max=255)])
    website = StringField('Website', validators=[Optional(), Length(max=255)])

    # Social media profiles
    facebook_profile = StringField('Facebook Profile', validators=[Optional(), Length(max=255)])
    twitter_profile = StringField('Twitter Profile', validators=[Optional(), Length(max=255)])
    linkedin_profile = StringField('LinkedIn Profile', validators=[Optional(), Length(max=255)])

    # Interests related to the user
    interests = StringField('Interests', validators=[Optional(), Length(max=255)])
    hobbies = StringField('Hobbies', validators=[Optional(), Length(max=255)])
