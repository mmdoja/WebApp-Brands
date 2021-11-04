import os
from flask import Flask
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from dotenv import load_dotenv
load_dotenv()
app = Flask(__name__)
app.config["MONGO_URI"] = os.environ.get('DB_URI')
app.config['MONGO_CONNECT']= False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SECURITY_PASSWORD_SALT'] = os.environ.get('SECURITY_PASSWORD_SALT')

mongo = PyMongo(app)
db_users = mongo.db.users
db_queries = mongo.db.queries
db_brands = mongo.db.brands
bcrypt = Bcrypt(app)
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
lm.login_message_category = 'info'

# mail settings
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

# gmail authentication
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
app.config['MAIL_DEFAULT_SENDER'] = 'QCXk4ThDa93pAnm@gmail.com'
mail = Mail(app)

from webappbackend import routes