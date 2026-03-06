from flask import render_template, redirect, url_for, flash, request
from app.admin import bp
from app.models.user import StaffUser
from app.models.customer import Customer
from app.admin.forms import StaffUserForm, LoginForm, CustomerForm
from app import db
from flask_login import login_required, login_user, logout_user, current_user

@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = StaffUserForm(obj=current_user)
    # Hide fields that aren't for self-management
    del form.username
    del form.nivel_etiqueta
    del form.nivel_numerico
    del form.activo
    
    if form.validate_on_submit():
        current_user.nombres = form.nombres.data
        current_user.apellidos = form.apellidos.data
        current_user.whatsapp = form.whatsapp.data
        current_user.fecha_nacimiento = form.fecha_nacimiento.data
        current_user.pin_rapido = form.pin_rapido.data
        current_user.cargo = form.cargo.data
        if form.password.data:
            current_user.set_password(form.password.data)
        db.session.commit()
        flash('Perfil actualizado exitosamente.')
        return redirect(url_for('admin.profile'))
    return render_template('admin/profile.html', title='Mi Perfil', form=form)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = StaffUser.query.filter_by(username=form.username.data).first()
        if user is None or not (user.check_password(form.password.data) or user.pin_rapido == form.password.data):
            flash('Usuario o credencial (Password/PIN) inválida.')
            return redirect(url_for('admin.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or not next_page.startswith('/'):
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('admin/login.html', title='Admin Login', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/staff')
@login_required
def staff_list():
    users = StaffUser.query.all()
    return render_template('admin/staff.html', title='Gestión de Staff', users=users)

@bp.route('/staff/new', methods=['GET', 'POST'])
@login_required
def staff_new():
    form = StaffUserForm()
    if form.validate_on_submit():
        user = StaffUser(
            username=form.username.data,
            nombres=form.nombres.data,
            apellidos=form.apellidos.data,
            whatsapp=form.whatsapp.data,
            fecha_nacimiento=form.fecha_nacimiento.data,
            pin_rapido=form.pin_rapido.data,
            cargo=form.cargo.data,
            nivel_etiqueta=form.nivel_etiqueta.data,
            nivel_numerico=int(form.nivel_numerico.data),
            activo=form.activo.data
        )
        if form.password.data:
            user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Usuario de staff creado exitosamente.')
        return redirect(url_for('admin.staff_list'))
    return render_template('admin/staff_form.html', title='Nuevo Miembro del Staff', form=form)

@bp.route('/staff/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def staff_edit(id):
    user = StaffUser.query.get_or_404(id)
    form = StaffUserForm(obj=user)
    if form.validate_on_submit():
        user.username = form.username.data
        user.nombres = form.nombres.data
        user.apellidos = form.apellidos.data
        user.whatsapp = form.whatsapp.data
        user.fecha_nacimiento = form.fecha_nacimiento.data
        user.pin_rapido = form.pin_rapido.data
        user.cargo = form.cargo.data
        user.nivel_etiqueta = form.nivel_etiqueta.data
        user.nivel_numerico = int(form.nivel_numerico.data)
        user.activo = form.activo.data
        if form.password.data:
            user.set_password(form.password.data)
        db.session.commit()
        flash('Staff actualizado.')
        return redirect(url_for('admin.staff_list'))
    return render_template('admin/staff_form.html', title='Editar Staff', form=form, user=user)

# --- Customer Management Hub ---

@bp.route('/customers')
@login_required
def customer_list():
    customers = Customer.query.all()
    return render_template('admin/customers.html', title='Cartera de Clientes', customers=customers)

@bp.route('/customers/new', methods=['GET', 'POST'])
@login_required
def customer_new():
    form = CustomerForm()
    if form.validate_on_submit():
        customer = Customer(
            codigo_unico=form.codigo_unico.data.strip() if form.codigo_unico.data else None,
            rfc=form.rfc.data.strip() if form.rfc.data else None,
            nombre_negocio=form.nombre_negocio.data,
            nombres=form.nombres.data,
            apellidos=form.apellidos.data,
            whatsapp=form.whatsapp.data,
            direccion=form.direccion.data,
            ruta_asignada=form.ruta_asignada.data,
            vendedor_asignado=form.vendedor_asignado.data,
            credito_asignado=float(form.credito_asignado.data.replace(',', '')) if form.credito_asignado.data and form.credito_asignado.data.strip() else 0.0,
            deuda_acumulada=float(form.deuda_acumulada.data.replace(',', '')) if form.deuda_acumulada.data and form.deuda_acumulada.data.strip() else 0.0,
            activo=form.activo.data
        )
        if form.password.data:
            customer.set_password(form.password.data)
        if form.pin_rapido.data:
            customer.pin_rapido = form.pin_rapido.data
            
        try:
            db.session.add(customer)
            db.session.commit()
            flash('Cliente registrado exitosamente.')
            return redirect(url_for('admin.customer_list'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al guardar cliente: {str(e)}')
            return redirect(url_for('admin.customer_new'))
    return render_template('admin/customer_form.html', title='Nuevo Cliente', form=form)

@bp.route('/customers/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def customer_edit(id):
    customer = Customer.query.get_or_404(id)
    # Prepare form with current data
    form = CustomerForm(obj=customer)
    if form.validate_on_submit():
        customer.codigo_unico = form.codigo_unico.data.strip() if form.codigo_unico.data else None
        customer.rfc = form.rfc.data.strip() if form.rfc.data else None
        customer.nombre_negocio = form.nombre_negocio.data
        customer.nombres = form.nombres.data
        customer.apellidos = form.apellidos.data
        customer.whatsapp = form.whatsapp.data
        customer.direccion = form.direccion.data
        customer.ruta_asignada = form.ruta_asignada.data
        customer.vendedor_asignado = form.vendedor_asignado.data
        customer.credito_asignado = float(form.credito_asignado.data.replace(',', '')) if form.credito_asignado.data and form.credito_asignado.data.strip() else 0.0
        customer.deuda_acumulada = float(form.deuda_acumulada.data.replace(',', '')) if form.deuda_acumulada.data and form.deuda_acumulada.data.strip() else 0.0
        customer.activo = form.activo.data
        
        if form.password.data:
            customer.set_password(form.password.data)
        if form.pin_rapido.data:
            customer.pin_rapido = form.pin_rapido.data
            
        try:
            db.session.commit()
            flash('Datos del cliente actualizados.')
            return redirect(url_for('admin.customer_list'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar cliente: {str(e)}')
            return redirect(url_for('admin.customer_edit', id=id))
    return render_template('admin/customer_form.html', title='Editar Cliente', form=form, customer=customer)
