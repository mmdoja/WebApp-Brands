from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateTimeField, RadioField, IntegerField, \
    FloatField, FieldList, validators
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional
from webappbackend import db_users

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = db_users.find_one({
            "username": username.data
        })
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = db_users.find_one({
            "email": email.data
        })
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = db_users.find_one({
            "email": email.data
        })
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        user = db_users.find_one({
            "username": username.data
        })
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = db_users.find_one({
            "email": email.data
        })
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class QueryForm(FlaskForm):
    brand = StringField('Brand', validators=[DataRequired(), Length(min=2, max=20)])

    product_name = StringField('Product Name', validators=[DataRequired(), Length(min=2, max=20)])

    max_pages = IntegerField('Max Pages')

    source = StringField('Source', validators=[Optional()])

    keyword_DE = StringField('Keyword DE', validators=[Optional()])
    keyword_UK = StringField('Keyword UK', validators=[Optional()])
    keyword_FR = StringField('Keyword FR', validators=[Optional()])
    keyword_IT = StringField('Keyword IT', validators=[Optional()])
    keyword_ES = StringField('Keyword ES', validators=[Optional()])

    asins_DE = StringField('Reference products DE', validators=[Optional()])
    asins_UK = StringField('Reference products UK', validators=[Optional()])
    asins_FR = StringField('Reference products FR', validators=[Optional()])
    asins_IT = StringField('Reference products IT', validators=[Optional()])
    asins_ES = StringField('Reference products ES', validators=[Optional()])

    reviews_seller_DE = IntegerField('Seller Review DE', validators=[Optional()])
    reviews_seller_UK = IntegerField('Seller Review UK', validators=[Optional()])
    reviews_seller_FR = IntegerField('Seller Review FR', validators=[Optional()])
    reviews_seller_IT = IntegerField('Seller Review IT', validators=[Optional()])
    reviews_seller_ES = IntegerField('Seller Review ES', validators=[Optional()])

    price_seller_DE = FloatField('Seller Price DE', validators=[Optional()])
    price_seller_UK = FloatField('Seller Price UK', validators=[Optional()])
    price_seller_FR = FloatField('Seller Price FR', validators=[Optional()])
    price_seller_IT = FloatField('Seller Price IT', validators=[Optional()])
    price_seller_ES = FloatField('Seller Price ES', validators=[Optional()])

    rating_seller_DE = FloatField('Seller Rating DE', validators=[Optional()])
    rating_seller_UK = FloatField('Seller Rating UK', validators=[Optional()])
    rating_seller_FR = FloatField('Seller Rating FR', validators=[Optional()])
    rating_seller_IT = FloatField('Seller Rating IT', validators=[Optional()])
    rating_seller_ES = FloatField('Seller Rating ES', validators=[Optional()])

    submit = SubmitField('Send')


class AddBrandName(FlaskForm):
    brand = StringField('Brand Name', validators=[DataRequired()])
    submit = SubmitField('Create Job')