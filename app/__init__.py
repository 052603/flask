# -*- coding: utf-8 -*- 
#from config import Flask
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager



loginmanager=LoginManager()
loginmanager.session_protection='strong'
loginmanager.login_view='user.login_index'



app = Flask(__name__)
app.config.from_object(Config)
#建立数据库关系
db = SQLAlchemy(app)
from app import models,view
#绑定app和数据库，以便进行操作
migrate = Migrate(app,db)
loginmanager.init_app(app)

def time_split(time):
	time_str = str(time)
	return time_str[0:19]

env = app.jinja_env
env.filters['time_split'] = time_split


