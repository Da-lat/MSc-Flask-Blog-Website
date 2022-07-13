from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, BooleanField
from wtforms.fields.choices import SelectField
from wtforms.fields.simple import BooleanField
from wtforms.validators import DataRequired, EqualTo, Length, ValidationError, Regexp, Email
from blog.models import User

class RegistrationForm(FlaskForm):
  first_name = StringField('First name',validators=[DataRequired(), Length(1,20), Regexp("^[a-zA-Z0-9_]*$", message="First name must contain only alphanumerical characters")])
  email = StringField('Email', validators=[DataRequired(), Length(1,64), Email(message="Invalid Email. Please check again")])
  password = PasswordField('Password',validators=[DataRequired(), Length(1,20), EqualTo('repeat_password', message='Passwords do not match. Please try again.' )])
  repeat_password = PasswordField('Repeat password',validators=[DataRequired(), Length(1,20), Regexp("^[a-zA-Z0-9_]*$", message="Your password contains invalid characters, please use alphanumerical characters only")])
  submit = SubmitField('Register')

  def validate_email(self, email):
    user = User.query.filter_by(email=email.data).first()
    if user is not None:
      raise ValidationError('This Email is already registered, please log in')

class LoginForm(FlaskForm):
  email = StringField('Email',validators=[DataRequired()])
  password = PasswordField('Password',validators=[DataRequired()])
  remember = BooleanField('Remember me')
  submit = SubmitField('Login')

class CommentForm(FlaskForm):
  body = TextAreaField(label='Please add a comment', validators=[DataRequired()])
  submit = SubmitField('Submit')

class RatingForm(FlaskForm):
  rating = SelectField("Please rate this post", choices=[int((1)),int((2)),int((3)),int((4)),int((5))], validators=[DataRequired()])
  submit = SubmitField('Submit rating')

class SortingForm(FlaskForm):
  sort = SelectField("Select an option to sort posts", choices=[("date_asc", "Sort by newest"), ("date_desc", "Sort by oldest")], validators=[DataRequired()])
  submit = SubmitField("Submit")