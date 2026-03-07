from flask import render_template, url_for, redirect, flash, request, session
from app.main import bp
from app.models.user import StaffUser
from app.models.customer import Customer
from app.admin.forms import CustomerForm
from app import db
from flask_login import login_required, login_user, logout_user, current_user
from app.models.subsystem import Subsystem

@bp.route('/')
@bp.route('/index')
def index():
    # Fetch active subsystems from database
    db_subsystems = Subsystem.query.filter_by(activo=True).all()
    
    # Base modules (can also be moved to DB eventually)
    modules = [
        {'title': 'Control de Negocios', 'description': 'Gestión integral de inventarios, ventas y proveedores.', 'route': '/negocios'},
    ]
    
    # Append dynamic subsystems
    for sub in db_subsystems:
        modules.append({
            'title': sub.nombre,
            'description': sub.descripcion or f"Subsistema activo en {sub.ruta}",
            'route': sub.ruta
        })
        
    return render_template('dashboard.html', title='Inicio', modules=modules)

# --- Authentication & Self-Management (Customers) ---

@bp.route('/customer/login', methods=['GET', 'POST'])
def customer_login():
    from app.admin.forms import CustomerLoginForm
    if current_user.is_authenticated and not getattr(current_user, 'is_staff', False):
        return redirect(url_for('main.index'))
    form = CustomerLoginForm()
    if form.validate_on_submit():
        customer = Customer.query.filter_by(codigo_unico=form.codigo_unico.data).first()
        # Customers can login with password or PIN (plain text check for PIN since it's short)
        if customer and (customer.check_password(form.password.data) or (customer.pin_rapido and customer.pin_rapido == form.password.data)):
            session['user_type'] = 'customer'
            login_user(customer, remember=form.remember_me.data)
            return redirect(url_for('main.index'))
        flash('Código Único o Credencial incorrecta.')
    return render_template('admin/customer_login.html', title='Portal Clientes', form=form)

@bp.route('/customer/profile', methods=['GET', 'POST'])
@login_required
def customer_profile():
    if current_user.is_staff:
        flash('Acceso exclusivo para clientes.')
        return redirect(url_for('admin.profile'))
        
    form = CustomerForm(obj=current_user)
    # Hide administrative fields
    del form.codigo_unico
    del form.rfc
    del form.nombre_negocio
    del form.credito_asignado
    del form.deuda_acumulada
    del form.ruta_asignada
    del form.vendedor_asignado
    del form.activo
    
    if form.validate_on_submit():
        current_user.nombres = form.nombres.data
        current_user.apellidos = form.apellidos.data
        current_user.whatsapp = form.whatsapp.data
        current_user.direccion = form.direccion.data
        current_user.pin_rapido = form.pin_rapido.data
        if form.password.data:
            current_user.set_password(form.password.data)
        db.session.commit()
        flash('Tu perfil ha sido actualizado.')
        return redirect(url_for('main.customer_profile'))
    return render_template('admin/customer_profile.html', title='Mi Perfil Cliente', form=form)

@bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    from app.admin.forms import ForgotPasswordForm
    import secrets
    import string
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        # Search in both Staff and Customers
        user = StaffUser.query.filter_by(whatsapp=form.whatsapp.data).first()
        is_staff_search = True
        if not user:
            user = Customer.query.filter_by(whatsapp=form.whatsapp.data).first()
            is_staff_search = False
            
        if user:
            # Generate temporary password
            temp_pass = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(8))
            user.set_password(temp_pass)
            db.session.commit()
            
            # Prepare WhatsApp message
            user_name = user.nombres if user.nombres else (user.username if is_staff_search else user.codigo_unico)
            message = f"Hola {user_name}, tu nueva clave temporal es: {temp_pass}. Por seguridad, cámbiala al entrar."
            whatsapp_url = f"https://wa.me/{user.whatsapp.replace('+', '').replace(' ', '')}?text={message.replace(' ', '%20')}"
            
            flash('Se ha generado una clave temporal. Haz clic en el link para enviarla por WhatsApp.')
            return render_template('admin/forgot_password_confirm.html', whatsapp_url=whatsapp_url)
            
        flash('No se encontró ningún usuario con ese número de WhatsApp.')
    return render_template('admin/forgot_password.html', title='Recuperar Acceso', form=form)
