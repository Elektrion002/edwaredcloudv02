from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from recompensas_app import db
from recompensas_app.models.customer import Customer
from recompensas_app.customer_forms import CustomerForm

bp = Blueprint('customer', __name__, url_prefix='/admin/customer')

@bp.route('/list')
@login_required
def list():
    customers = Customer.query.all()
    return render_template('customer/list.html', title='Gestión de Clientes', customers=customers)

@bp.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    form = CustomerForm()
    if form.validate_on_submit():
        customer = Customer(
            cliente_id=form.cliente_id.data,
            nombres=form.nombres.data,
            apellidos=form.apellidos.data,
            celular_whatsapp=form.celular_whatsapp.data,
            direccion_fisica=form.direccion_fisica.data,
            credencial_id=Customer.generate_credencial_id(),
            activo=form.activo.data
        )
        if form.password.data:
            customer.set_password(form.password.data)
        if form.pin.data:
            customer.set_pin(form.pin.data)
            
        db.session.add(customer)
        db.session.commit()
        flash(f'Cliente {customer.cliente_id} registrado exitosamente.', 'success')
        return redirect(url_for('customer.list'))
    
    return render_template('customer/customer_form.html', title='Registrar Nuevo Cliente', form=form)

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    customer = Customer.query.get_or_404(id)
    form = CustomerForm(original_cliente_id=customer.cliente_id, original_whatsapp=customer.celular_whatsapp)
    
    if form.validate_on_submit():
        customer.cliente_id = form.cliente_id.data
        customer.nombres = form.nombres.data
        customer.apellidos = form.apellidos.data
        customer.celular_whatsapp = form.celular_whatsapp.data
        customer.direccion_fisica = form.direccion_fisica.data
        customer.activo = form.activo.data
        
        if form.password.data:
            customer.set_password(form.password.data)
        if form.pin.data:
            customer.set_pin(form.pin.data)
            
        db.session.commit()
        flash(f'Cliente {customer.cliente_id} actualizado.', 'success')
        return redirect(url_for('customer.list'))
    
    elif request.method == 'GET':
        form.cliente_id.data = customer.cliente_id
        form.nombres.data = customer.nombres
        form.apellidos.data = customer.apellidos
        form.celular_whatsapp.data = customer.celular_whatsapp
        form.direccion_fisica.data = customer.direccion_fisica
        form.activo.data = customer.activo
        
    return render_template('customer/customer_form.html', title='Editar Cliente', form=form)
