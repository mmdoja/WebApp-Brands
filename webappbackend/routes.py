from flask import render_template, url_for, flash, redirect, request
from webappbackend import app, mongo, bcrypt, db_operations, lm
from webappbackend.forms import RegistrationForm, LoginForm
from webappbackend.token import generate_confirmation_token, confirm_token
import re
from .user import User
from .email import send_email
from flask_login import login_required


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
            token = generate_confirmation_token(form.email.data)
            flash(f'You have been logged in {token}', 'success')
            #return redirect(url_for('confirmemail'))
            confirm_url = url_for('confirm_email', token=token, _external=True)
            html = render_template('activate.html', confirm_url=confirm_url)
            subject = "Please confirm your email"
            send_email(form.email.data, subject, html)

            #login_user(user)

            flash('A confirmation email has been sent via email.', 'success')
            return redirect(url_for("confirmemail"))
    return render_template('register.html', title='Register', form=form)

@lm.user_loader
def load_user(username):
    u = db_operations.find_one({"_id": username})
    if not u:
        return None
    return User(u['_id'])

@app.route('/confirm/<token>')
@login_required
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
    user = db_operations.find_one({"email":email})
    if user.confirmed:
        flash('Account already confirmed. Please login.', 'success')
    else:
        #user.confirmed = True
        #db_operations.insert_one(new_user)
        flash('You have confirmed your account. Thanks!', 'success')
    return redirect(url_for('home'))



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
