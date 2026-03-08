from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from recompensas_app import db
from recompensas_app.models.customer import Customer
from recompensas_app.models.movement import Movement
from recompensas_app.models.product import Product
from recompensas_app.portal_forms import CustomerPortalLoginForm, CustomerUpdateSecretForm, CustomerRecoveryForm

from recompensas_app.utils.security import check_rate_limit, record_auth_fail, clear_auth_history

portal_bp = Blueprint('portal', __name__, url_prefix='/portal')

@portal_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if hasattr(current_user, 'cliente_id'):
            return redirect(url_for('portal.dashboard'))
        logout_user()

    form = CustomerPortalLoginForm()
    
    # Check Rate Limit
    is_allowed, info = check_rate_limit()
    
    if not is_allowed:
        flash(f'Demasiados intentos fallidos. Por seguridad, tu acceso está bloqueado por {info} minutos más.', 'danger')
        return render_template('portal/login.html', title='Portal Bloqueado', form=form, blocked=True)

    if form.validate_on_submit():
        customer = Customer.query.filter_by(cliente_id=form.cliente_id.data).first()
        if customer:
            secret = form.secret.data
            is_valid = False
            
            if customer.password_hash and customer.check_password(secret):
                is_valid = True
            elif secret.isdigit() and 4 <= len(secret) <= 10:
                if customer.pin_hash and customer.check_pin(secret):
                    is_valid = True
            
            if is_valid:
                clear_auth_history()
                login_user(customer, remember=form.remember_me.data)
                return redirect(url_for('portal.dashboard'))
        
        record_auth_fail()
        flash('Credenciales inválidas. Verifica tu ID y clave/PIN.', 'danger')
    
    return render_template('portal/login.html', title='Portal del Cliente', form=form)

@portal_bp.route('/dashboard')
@login_required
def dashboard():
    if not hasattr(current_user, 'cliente_id'):
        flash('Esta área es exclusiva para clientes.', 'warning')
        return redirect(url_for('main.index'))
    
    # Generar URL del QR (usando el credencial_id)
    qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={current_user.credencial_id}"
    
    return render_template('portal/dashboard.html', title='Mi Credencial', qr_url=qr_url)

@portal_bp.route('/history')
@login_required
def history():
    if not hasattr(current_user, 'cliente_id'):
        return redirect(url_for('main.index'))
    
    movements = current_user.movements.order_by(Movement.created_at.desc()).all()
    return render_template('portal/history.html', title='Mis Movimientos', movements=movements)

@portal_bp.route('/catalog')
@login_required
def catalog():
    if not hasattr(current_user, 'cliente_id'):
        return redirect(url_for('main.index'))
    
    # Solo productos activos y ordenados por tipo/categoría
    products = Product.query.filter_by(activo=True).order_by(Product.tipo_producto, Product.descripcion).all()
    return render_template('portal/catalog.html', title='Catálogo de Recompensas', products=products)

@portal_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if not hasattr(current_user, 'cliente_id'):
        return redirect(url_for('main.index'))
        
    form = CustomerUpdateSecretForm()
    if form.validate_on_submit():
        # Validar clave actual
        valid_current = False
        if current_user.password_hash and current_user.check_password(form.current_secret.data):
            valid_current = True
        elif form.current_secret.data.isdigit() and current_user.pin_hash and current_user.check_pin(form.current_secret.data):
            valid_current = True
            
        if valid_current:
            if form.new_password.data:
                current_user.set_password(form.new_password.data)
            if form.new_pin.data:
                current_user.set_pin(form.new_pin.data)
            db.session.commit()
            flash('Seguridad actualizada exitosamente.', 'success')
            return redirect(url_for('portal.dashboard'))
        else:
            flash('La clave actual es incorrecta.', 'danger')
            
    return render_template('portal/profile.html', title='Mi Perfil', form=form)

@portal_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('portal.login'))

@portal_bp.route('/recovery', methods=['GET', 'POST'])
def recovery():
    form = CustomerRecoveryForm()
    if form.validate_on_submit():
        customer = Customer.query.filter_by(celular_whatsapp=form.celular_whatsapp.data).first()
        if customer:
            # Generar link de WhatsApp
            msg = f"Hola, solicito recuperar mi acceso al Portal de Recompensas. Mi ID es {customer.cliente_id}."
            wa_link = f"https://wa.me/523121550543?text={msg.replace(' ', '%20')}" # Número de admin por defecto
            return redirect(wa_link)
        flash('No encontramos una cuenta con ese número.', 'warning')
    return render_template('portal/recovery.html', title='Recuperar Acceso', form=form)
