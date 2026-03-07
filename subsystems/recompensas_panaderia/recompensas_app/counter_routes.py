from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from recompensas_app import db
from recompensas_app.models.customer import Customer
from recompensas_app.models.movement import Movement
from datetime import datetime

bp = Blueprint('counter', __name__, url_prefix='/admin/counter')

@bp.route('/')
@login_required
def index():
    return render_template('admin/counter.html', title='Mostrador de Recompensas')

@bp.route('/search')
@login_required
def search():
    query = request.args.get('q', '').strip()
    if not query:
        return jsonify([])
    
    # Búsqueda por Celular, Nombre o Apellido, o ID de Credencial
    customers = Customer.query.filter(
        (Customer.celular_whatsapp.contains(query)) |
        (Customer.nombres.ilike(f'%{query}%')) |
        (Customer.apellidos.ilike(f'%{query}%')) |
        (Customer.cliente_id.ilike(f'%{query}%')) |
        (Customer.credencial_id == query)
    ).filter_by(activo=True).limit(10).all()
    
    results = []
    for c in customers:
        results.append({
            'id': c.id,
            'cliente_id': c.cliente_id,
            'nombre_completo': f"{c.nombres} {c.apellidos}",
            'celular': c.celular_whatsapp,
            'puntos': c.puntos_disponibles
        })
    
    return jsonify(results)

@bp.route('/operate', methods=['POST'])
@login_required
def operate():
    customer_id = request.form.get('customer_id')
    tipo = request.form.get('tipo') # 'acumulacion' or 'canje'
    puntos = request.form.get('puntos', type=int)
    concepto = request.form.get('concepto', 'Operación en mostrador')
    
    if not customer_id or not tipo or puntos is None or puntos <= 0:
        return jsonify({'success': False, 'message': 'Datos inválidos'}), 400
    
    customer = Customer.query.get_or_404(customer_id)
    
    if tipo == 'canje' and customer.puntos_disponibles < puntos:
        return jsonify({'success': False, 'message': 'Saldo de puntos insuficiente'}), 400
    
    try:
        if tipo == 'acumulacion':
            customer.puntos_disponibles += puntos
        elif tipo == 'canje':
            customer.puntos_disponibles -= puntos
            customer.puntos_canjeados += puntos
        
        # Registrar movimiento
        movement = Movement(
            customer_id=customer.id,
            tipo=tipo,
            puntos=puntos,
            concepto=concepto,
            saldo_resultante=customer.puntos_disponibles,
            staff_id=current_user.id
        )
        
        db.session.add(movement)
        db.session.commit()
        
        return jsonify({
            'success': True, 
            'message': 'Operación realizada con éxito',
            'nuevo_saldo': customer.puntos_disponibles
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500
