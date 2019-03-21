from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_pagedown import PageDown
from flaskext.markdown import Markdown

pagedown = PageDown()
db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
bootstrap = Bootstrap()


def create_app(settings):
    app = Flask(__name__, instance_relative_config=True)
    app.config.update(settings)

    initialize_extensions(app)
    register_blueprints(app)

    return app


def initialize_extensions(app):
    pagedown.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    login.login_view = 'login'
    bootstrap.init_app(app)
    Markdown(app)


def register_blueprints(flask_app):
    from app.admin import admin_blueprint
    from app.blog import blog_blueprint

    flask_app.register_blueprint(admin_blueprint)
    flask_app.register_blueprint(blog_blueprint)
