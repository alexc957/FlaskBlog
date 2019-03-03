# we initialize the app

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
#an instance of flask
# __name__ the name of this module
app = Flask(__name__)

app.config['SECRET_KEY']= '5909ecfe0f7ffa554b4d2c0f37dc8ff6'
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager  =LoginManager(app)
login_manager.login_view = 'login' #function name fo login
login_manager.login_message_category = 'info' 
from flaskblog import routes
