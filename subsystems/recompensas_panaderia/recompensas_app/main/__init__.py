from flask import Blueprint

bp = Blueprint('main', __name__)

from recompensas_app.main import routes
