from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_fontawesome import FontAwesome
from flask_pagedown import PageDown
from flaskext.markdown import Markdown

from settings import SETTINGS

app = Flask(__name__)
app.config.update(SETTINGS)
Markdown(app)
pagedown = PageDown(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
bootstrap = Bootstrap(app)
fa = FontAwesome(app)

from app import routes, models
