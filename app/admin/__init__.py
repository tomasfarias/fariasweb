from flask import Blueprint

admin_blueprint = Blueprint('admin', __name__, static_folder='static', template_folder='templates')

from . import routes
