# we initialize the app

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

import os
#an instance of flask
# __name__ the name of this module
app = Flask(__name__)

#app.config['SECRET_KEY']= 'the-secret-key-goes-here'
app.config['SECRET_KEY']=os.environ.get('SECRET_KEY') or "my-secret-key"
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager  =LoginManager(app)
login_manager.login_view = 'users.login' #function name fo login
login_manager.login_message_category = 'info'


from flaskblog.users.routes import users
from flaskblog.posts.routes import posts
from flaskblog.main.routes import main

app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(main)
