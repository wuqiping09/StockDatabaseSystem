import os
from flask import Flask,Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from config import Config, basedir

app = Flask(__name__)

app.config.from_object(Config)
app.config.setdefault('BOOTSTRAP_SERVE_LOCAL', True)    #从本地加载bootstrap
db = SQLAlchemy(app)
db.create_all()
migrate = Migrate(app, db)
login = LoginManager(app)
login.init_app(app)
login.login_message = u'请先登录！'
login.login_view = 'account.login'

bootstrap = Bootstrap(app)
