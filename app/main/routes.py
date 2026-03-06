from flask import render_template, url_for
from app.main import bp

@bp.route('/')
@bp.route('/index')
def index():
    modules = [
        {'title': 'Control de Negocios', 'description': 'Gestión integral de inventarios, ventas y proveedores.', 'route': '/negocios'},
        {'title': 'Programa de Recompensas', 'description': 'Sistema de fidelización y puntos para clientes.', 'route': '/recompensas'}
    ]
    return render_template('dashboard.html', title='Inicio', modules=modules)
