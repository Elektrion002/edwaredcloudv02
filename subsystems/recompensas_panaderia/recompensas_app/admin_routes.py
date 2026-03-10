from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from recompensas_app import db
from recompensas_app.models.customer import Customer
from recompensas_app.models.movement import Movement
from recompensas_app.models.staff import StaffUser
from recompensas_app.decorators import admin_required
from sqlalchemy import func, desc
from datetime import datetime, timedelta

admin_bp = Blueprint('admin', __name__, url_prefix='/admin/stats')

@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    # 1. KPIs Generales
    total_acumulacion = db.session.query(func.sum(Movement.puntos)).filter(Movement.tipo == 'acumulacion').scalar() or 0
    total_canje = db.session.query(func.sum(Movement.puntos)).filter(Movement.tipo == 'canje').scalar() or 0
    
    # Asumiendo una tasa de valor: 100 puntos = 1 USD (o moneda local)
    # Esto es demostrativo, se puede ajustar
    dinero_canjeado = total_canje / 100 
    compras_generadoras = db.session.query(func.count(Movement.id)).filter(Movement.tipo == 'acumulacion').scalar() or 0

    # 2. Tops de Clientes
    # Top clientes puntos generados
    top_clientes_ganan = db.session.query(
        Customer.nombres, Customer.apellidos, func.sum(Movement.puntos).label('total')
    ).join(Movement, Customer.id == Movement.customer_id)\
     .filter(Movement.tipo == 'acumulacion')\
     .group_by(Customer.id)\
     .order_by(desc('total'))\
     .limit(5).all()

    # Top clientes que canjean
    top_clientes_canje = db.session.query(
        Customer.nombres, Customer.apellidos, func.sum(Movement.puntos).label('total')
    ).join(Movement, Customer.id == Movement.customer_id)\
     .filter(Movement.tipo == 'canje')\
     .group_by(Customer.id)\
     .order_by(desc('total'))\
     .limit(5).all()

    # 3. Tops de Staff
    # Top usuarios que asignan puntos
    top_staff_asigna = db.session.query(
        StaffUser.username, func.sum(Movement.puntos).label('total')
    ).join(Movement, StaffUser.id == Movement.staff_id)\
     .filter(Movement.tipo == 'acumulacion')\
     .group_by(StaffUser.id)\
     .order_by(desc('total'))\
     .limit(5).all()

    # Top usuarios que canjean
    top_staff_canje = db.session.query(
        StaffUser.username, func.sum(Movement.puntos).label('total')
    ).join(Movement, StaffUser.id == Movement.staff_id)\
     .filter(Movement.tipo == 'canje')\
     .group_by(StaffUser.id)\
     .order_by(desc('total'))\
     .limit(5).all()

    return render_template('admin/dashboard.html', 
                           title='Dashboard de Inteligencia',
                           kpis={
                               'total_acumulacion': total_acumulacion,
                               'total_canje': total_canje,
                               'dinero_canjeado': dinero_canjeado,
                               'compras_generadoras': compras_generadoras
                           },
                           tops={
                               'clientes_ganan': top_clientes_ganan,
                               'clientes_canje': top_clientes_canje,
                               'staff_asigna': top_staff_asigna,
                               'staff_canje': top_staff_canje
                           })

@admin_bp.route('/kardex')
@login_required
@admin_required
def kardex():
    periodo = request.args.get('periodo', 'historico')
    query = Movement.query.order_by(Movement.created_at.desc())
    
    now = datetime.utcnow()
    if periodo == 'hoy':
        query = query.filter(Movement.created_at >= now.replace(hour=0, minute=0, second=0, microsecond=0))
    elif periodo == 'ayer':
        ayer = now - timedelta(days=1)
        query = query.filter(Movement.created_at >= ayer.replace(hour=0, minute=0, second=0, microsecond=0),
                             Movement.created_at < now.replace(hour=0, minute=0, second=0, microsecond=0))
    elif periodo == 'semana':
        semana = now - timedelta(days=7)
        query = query.filter(Movement.created_at >= semana)
    
    # Búsqueda por cliente
    search = request.args.get('q', '').strip()
    if search:
        query = query.join(Customer).filter(
            (Customer.nombres.ilike(f'%{search}%')) | 
            (Customer.apellidos.ilike(f'%{search}%')) |
            (Customer.cliente_id.ilike(f'%{search}%'))
        )

    movements = query.all()
    
    # Para mostrar nombres de staff en el Kardex
    staff_map = {u.id: u.username for u in StaffUser.query.all()}
    
    return render_template('admin/kardex.html', 
                           title='Kardex Histórico',
                           movements=movements,
                           staff_map=staff_map,
                           periodo=periodo,
                           search=search)
