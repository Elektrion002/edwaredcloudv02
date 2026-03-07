from flask import render_template
from flask_login import login_required
from recompensas_app.main import bp

@bp.route('/')
@bp.route('/index')
@login_required
def index():
    return "Bienvenido al Subsistema de Recompensas - Panadería Demo"
