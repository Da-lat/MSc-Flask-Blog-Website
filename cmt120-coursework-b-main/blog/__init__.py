from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = ''

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://USERNAME:PASSWORD@csmysql.cs.cf.ac.uk:3306/USERNAME_DATABASE_NAME'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://USERNAME:PASSWORD@csmysql.cs.cf.ac.uk:3306/c21118494_Flask_lab_db'

app.config['FLASKY_COMMENTS_PER_PAGE'] = 10
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

from blog import routes
from .models import *
