from flask import Blueprint

blog_blueprint = Blueprint('blog', __name__, static_folder='static', template_folder='templates')

from . import routes
