from flask import render_template, url_for, flash, redirect, request
from webappbackend import app, mongo, bcrypt, db_operations
from webappbackend.forms import RegistrationForm, LoginForm
import re
#from flask_login import login_user, current_user, logout_user, login_required


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


@app.route("/confirmemail")
def confirmemail():
    return render_template('emailconfirmation.html', title='Confirm email')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if re.search('[a-zA-Z0-9]*@amazingbrands.group', form.email.data):
            flash(f'Account created for {form.username.data}!', 'success')
            new_user = {'username' : form.username.data, 'email' :form.email.data, 'password':form.password.data}
            db_operations.insert_one(new_user)
            return redirect(url_for('confirmemail'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)
