import subprocess
from os import abort
from time import time
from datetime import datetime
from bson import ObjectId
from flask import render_template, url_for, flash, redirect, request, session, jsonify, send_from_directory
from webappbackend import app, bcrypt, db_users, lm, db_queries, db_brands
from webappbackend.forms import RegistrationForm, LoginForm, RequestResetForm, ResetPasswordForm, UpdateAccountForm, \
    RunScraper
from webappbackend.forms import AddBrandName
from webappbackend.token import generate_confirmation_token, generate_password_reset_token, confirm_token
import re
from .user import User
from .email import send_email
from flask_login import login_required, current_user, login_user, logout_user


if __name__ == '__main__':
    app.run(debug=True)


posts = [
    {
        'name': 'Janik Euskirchen',
        'linkedin': 'https://www.linkedin.com/in/janikeuskirchen/',
        'position': 'Data Scientist and Software Developer',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'name': 'Mohammad Munirud Doja',
        'linkedin': 'https://www.linkedin.com/in/mohammadmuniruddoja/',
        'position': 'Software Developer',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    },
{
        'name': 'Zakir Ayub Bhuiyan',
        'linkedin': 'https://www.linkedin.com/in/zakir-tushar/',
        'position': 'Software Developer',
        'content': 'Third post content',
        'date_posted': 'April 21, 2018'
    },
{
        'name': 'Divyanshu Katiyar',
        'linkedin': 'https://www.linkedin.com/in/divyanshu-katiyar-45ba03131/',
        'position': 'Data Scientist',
        'content': 'Fourth post content',
        'date_posted': 'April 21, 2018'
    },
{
        'name': 'Nadezda Tyulneva',
        'linkedin': 'https://www.linkedin.com/in/nadezda-tyulneva-85057315b/',
        'position': 'Data Scientist',
        'content': 'Fifth post content',
        'date_posted': 'April 21, 2018'
    }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template('index.html', posts=posts)


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
            db_users.insert_one(new_user)
            db_users.update(
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
    user_json = db_users.find_one({'_id': ObjectId(user_id)})
    return User(user_json)

@app.route("/confirm/<token>")
def confirm_email(token):
    email = confirm_token(token)
    user = db_users.find_one({
        "email": email
    })
    db_users.update(
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
        user = db_users.find_one({
            "email": form.email.data
        })
        if user and bcrypt.check_password_hash(user['password'], form.password.data) and user['confirmed'] is True:
            flash('You have been logged in!', 'success')
            login_user(User(user))
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('jobs'))
        else:
            flash('Login Unsuccessful. Please check email id and password', 'danger')
    return render_template('login.html', title='Login', form=form)


#logout route
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route("/forgot-password", methods=['GET', 'POST'])
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
    return render_template('forgot-password.html', title='Reset Password', form=form)


@app.route("/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    email = confirm_token(token)
    user = db_users.find_one({
        "email": email
    })
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        filt = {"$set": {'password': hashed_password}}
        db_users.update_one(user, filt)
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('reset_password.html', title='Reset Password', form=form)


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    user = db_users.find_one({
            "_id": ObjectId(session['_user_id'])
        })
    form = UpdateAccountForm()
    if form.validate_on_submit():
        filt = {"$set": {'username': form.username.data, 'email': form.email.data}}
        db_users.update_one(user, filt)
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = user['username']
        form.email.data = user['email']
    return render_template('account.html', user=user, title='Account', form=form)


def del_none(query):
    for key, value in list(query.items()):
        if value is None or value == "" or value == [""] or value == 0:
            del query[key]
        elif isinstance(value, dict):
            del_none(value)
    return query


@app.route("/add_brand", methods=['GET', 'POST'])
@login_required
def create_job():
    form = AddBrandName()
    brand = {'brand': form.brand.data, 'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    if form.validate_on_submit():
        db_brands.insert_one(brand)
        flash('Job Created', 'success')
        return redirect(url_for('jobs'))
    return render_template('add_brand.html', form=form)


@app.route("/jobs", methods=['GET', 'POST'])
@login_required
def jobs():
    cursor = db_brands.aggregate(
        [
            {"$sort": {'date': -1}}
        ]
    )
    item=[]
    for document in cursor:
        an_item = dict(brand=document.get('brand'), date=document.get('date'))
        item.append(an_item)
    form = RunScraper()
    if form.validate_on_submit():
        print('Scraper running clicked')
        filename = "query_Swingfit.hjson"
        subprocess.run('cd .. && cd marketplace-analysis && python3 Scraper.py %s'%filename,
                       shell=True, universal_newlines=True)
    return render_template('tables.html', title='Jobs', form=form, item=item)


@app.route('/query')
@login_required
def query_page():
    return render_template('newQueryFile.html')


@app.route("/submitQuery", methods=["POST", "GET"])
def query():
    if request.method == 'POST':
        brandName = request.form.get('brandName')
        productName = request.form.getlist('productName[]')
        maxPages = request.form.getlist('maxPages[]')

        keywordDE = request.form.getlist('keywordDE[]')
        keywordUK = request.form.getlist('keywordUK[]')
        keywordFR = request.form.getlist('keywordFR[]')
        keywordIT = request.form.getlist('keywordIT[]')
        keywordES = request.form.getlist('keywordES[]')

        asinDE = request.form.getlist('asinDE[]')
        asinUK = request.form.getlist('asinUK[]')
        asinFR = request.form.getlist('asinFR[]')
        asinIT = request.form.getlist('asinIT[]')
        asinES = request.form.getlist('asinES[]')

        reviewDE = request.form.getlist('reviewDE[]')
        reviewUK = request.form.getlist('reviewUK[]')
        reviewFR = request.form.getlist('reviewFR[]')
        reviewIT = request.form.getlist('reviewIT[]')
        reviewES = request.form.getlist('reviewES[]')

        priceDE = request.form.getlist('priceDE[]')
        priceUK = request.form.getlist('priceUK[]')
        priceFR = request.form.getlist('priceFR[]')
        priceIT = request.form.getlist('priceIT[]')
        priceES = request.form.getlist('priceES[]')

        ratingDE = request.form.getlist('ratingDE[]')
        ratingUK = request.form.getlist('ratingUK[]')
        ratingFR = request.form.getlist('ratingFR[]')
        ratingIT = request.form.getlist('ratingIT[]')
        ratingES = request.form.getlist('ratingES[]')

        msg = 'New query created successfully'
        flag = 0
        product = {}
        while(flag<len(productName)):
            keywords = {
                'DE': [x.strip() for x in keywordDE[flag].split(',')],
                'UK': [x.strip() for x in keywordUK[flag].split(',')],
                'FR': [x.strip() for x in keywordFR[flag].split(',')],
                'IT': [x.strip() for x in keywordIT[flag].split(',')],
                'ES': [x.strip() for x in keywordES[flag].split(',')],
            }
            asins = {
                'DE': [x.strip() for x in asinDE[flag].split(',')],
                'UK': [x.strip() for x in asinUK[flag].split(',')],
                'FR': [x.strip() for x in asinFR[flag].split(',')],
                'IT': [x.strip() for x in asinIT[flag].split(',')],
                'ES': [x.strip() for x in asinES[flag].split(',')],
            }
            reviews_seller = {
                'DE': float(reviewDE[flag].strip() or 0.0),
                'UK': float(reviewUK[flag].strip() or 0.0),
                'FR': float(reviewFR[flag].strip() or 0.0),
                'IT': float(reviewIT[flag].strip() or 0.0),
                'ES': float(reviewES[flag].strip() or 0.0),
            }
            price_seller = {
                'DE': float(priceDE[flag].strip() or 0.0),
                'UK': float(priceUK[flag].strip() or 0.0),
                'FR': float(priceFR[flag].strip() or 0.0),
                'IT': float(priceIT[flag].strip() or 0.0),
                'ES': float(priceES[flag].strip() or 0.0),
            }
            rating_seller = {
                'DE': float(ratingDE[flag].strip() or 0.0),
                'UK': float(ratingUK[flag].strip() or 0.0),
                'FR': float(ratingFR[flag].strip() or 0.0),
                'IT': float(ratingIT[flag].strip() or 0.0),
                'ES': float(ratingES[flag].strip() or 0.0),
            }
            query_1 = {
                'max_pages': float(maxPages[flag].strip() or 0.0),
                'keywords': keywords,
                'asins': asins,
                'reviews_seller': reviews_seller,
                'price_seller': price_seller,
                'rating_seller': rating_seller
            }
            product.update({
                productName[flag]: query_1
            })
            complete_query = {
                'brand': brandName,
                'queries': product
            }
            flag=flag+1
        print(del_none(complete_query))
        timestamp = int(time())
        filename = f"query_{brandName}_{timestamp}"
        with open(f"webappbackend/static/queries/{filename}.hjson", "w+") as fo:
            fo.write(str(del_none(complete_query)))
        db_queries.insert_one(del_none(complete_query))
        return jsonify(msg)


@app.route('/downloadfile')
def download_file():
    brand = 'Nordic'
    cursor = db_queries.find({
        'brand': brand
    })
    for document in cursor:
        print(document)
        with open(f"queries/test.csv", 'w+') as f:
            f.write(str(document))
    return redirect(url_for('jobs'))

'''
DOWNLOAD_DIRECTORY = "/home/mmdoja/webapp-backend/webappbackend/static/queries"
@app.route('/get-files/<path>',methods = ['GET','POST'])
def get_files(path):
    """Download a file."""
    try:
        return send_from_directory(DOWNLOAD_DIRECTORY, path, as_attachment=True)
    except FileNotFoundError:
        abort(404)
'''

@app.route('/test')
def test():
    return render_template('test.html')