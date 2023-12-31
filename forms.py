from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, SubmitField, PasswordField, DateField, TextAreaField, FileField, MultipleFileField, \
    validators
from wtforms.validators import DataRequired, URL, Length, EqualTo, Optional, ValidationError
from flask_ckeditor import CKEditorField
from PIL import Image


# Login form ----------------------------------------------------
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
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
    images = MultipleFileField('Files', validators=[
        validators.Length(max=10, message="You can upload a maximum of 10 files."),
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Only image files are allowed.')
    ])
    content = CKEditorField("Post Content", validators=[DataRequired()])
    submit = SubmitField("Post")


# Comment form ----------------------------------------------------
class CommentForm(FlaskForm):
    content = CKEditorField("Comment Content", validators=[DataRequired()])
    submit = SubmitField("Post")


# Profile Form ----------------------------------------------------
class UserProfileForm(FlaskForm):
    profile_img = FileField('Profile Picture')
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
    submit = SubmitField("Submit")

    # Todo: validate profile image
    # def validate_image(self, field):
    #     if field.data:
    #         self.profile_img = Image.open(field.data)
    #         max_width = 600  # Set your maximum width
    #         max_height = 600  # Set your maximum height
    #
    #         if self.profile_img.width > max_width or self.profile_img.height > max_height:
    #             raise ValidationError(f'Image dimensions must be at most {max_width}x{max_height} pixels.')


class CommunityForm(FlaskForm):

    name = StringField('Community Name', validators=[DataRequired(), Length(max=25)])
    description = StringField('Community Description', validators=[Length(max=250)])
    picture = FileField('Community Picture')

    submit = SubmitField("Submit")
