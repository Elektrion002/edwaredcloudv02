from flask import render_template, redirect, url_for, flash, request
from app.admin import bp
from app.models.user import StaffUser
from app.admin.forms import StaffUserForm
from app import db
from flask_login import login_required, login_user, logout_user, current_user
from app.admin.forms import StaffUserForm, LoginForm

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
