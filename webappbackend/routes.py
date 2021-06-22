from bson import ObjectId
from flask import render_template, url_for, flash, redirect, request, session
from webappbackend import app, bcrypt, db_operations, lm
from webappbackend.forms import RegistrationForm, LoginForm, RequestResetForm, ResetPasswordForm, UpdateAccountForm
from webappbackend.token import generate_confirmation_token, generate_password_reset_token, confirm_token
import re
from .user import User
from .email import send_email
from flask_login import login_required, current_user, login_user, logout_user


posts = [
    {
        'name': 'Janik Euskirchen',
        'position': 'Data Scientist and Software Developer',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'name': 'Mohammad Munirud Doja',
        'position': 'Software Developer',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')

#register route
@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        if re.search('[a-zA-Z0-9]*@amazingbrands.group', form.email.data):
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            new_user = {'username': form.username.data, 'email': form.email.data, 'password': hashed_password}
            db_operations.insert_one(new_user)
            db_operations.update(
                new_user, { "$set": {'confirmed': False}}
            )
            token = generate_confirmation_token(form.email.data)
            confirm_url = url_for('confirm_email', token=token, _external=True)
            html = render_template('activate.html', confirm_url=confirm_url)
            subject = "Please confirm your email"
            send_email(form.email.data, subject, html)
            flash('A confirmation email has been sent to your email address.', 'success')
            return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@lm.user_loader
def load_user(user_id):
    user_json = db_operations.find_one({'_id': ObjectId(user_id)})
    return User(user_json)

@app.route("/confirm/<token>")
def confirm_email(token):
    email = confirm_token(token)
    user = db_operations.find_one({
        "email": email
    })
    db_operations.update(
        user, {"$set": {'confirmed': True}}
    )
    flash('Your account has been confirmed. Please login', 'success')
    return redirect(url_for('login'))


#login route
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db_operations.find_one({
            "email": form.email.data
        })
        if user and bcrypt.check_password_hash(user['password'], form.password.data) and user['confirmed'] is True:
            flash('You have been logged in!', 'success')
            login_user(User(user))
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email id and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        token = generate_password_reset_token(form.email.data)
        confirm_url = url_for('reset_token', token=token, _external=True)
        html = render_template('password_reset.html', confirm_url=confirm_url)
        subject = "Password Reset"
        send_email(form.email.data, subject, html)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    email = confirm_token(token)
    user = db_operations.find_one({
        "email": email
    })
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        filt = {"$set": {'password': hashed_password}}
        db_operations.update_one(user, filt)
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('reset_password.html', title='Reset Password', form=form)


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    user = db_operations.find_one({
            "_id": ObjectId(session['_user_id'])
        })
    form = UpdateAccountForm()
    if form.validate_on_submit():
        filt = {"$set": {'username': form.username.data, 'email': form.email.data}}
        db_operations.update_one(user, filt)
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = user['username']
        form.email.data = user['email']
    return render_template('account.html', user=user, title='Account', form=form)