from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from recompensas_app import db
from recompensas_app.models.staff import StaffUser
from recompensas_app.auth_forms import StaffUserForm
from datetime import datetime

staff_bp = Blueprint('staff', __name__)

@staff_bp.route('/list')
@login_required
def list():
    if current_user.nivel_numerico > 30: # Solo Admin o superior
        flash('No tienes permisos para acceder a esta sección.', 'error')
        return redirect(url_for('main.index'))
    
    users = StaffUser.query.all()
    return render_template('staff/list.html', users=users)

@staff_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    if current_user.nivel_numerico > 20: # Solo Super Admin o Admin
        flash('No tienes permisos para crear usuarios.', 'error')
        return redirect(url_for('staff.list'))
    
    form = StaffUserForm()
    if form.validate_on_submit():
        user = StaffUser(
            username=form.username.data,
            nombres=form.nombres.data,
            apellidos=form.apellidos.data,
            celular_whatsapp=form.celular_whatsapp.data,
            fecha_nacimiento=form.fecha_nacimiento.data,
            cargo=form.cargo.data,
            nivel_usuario=form.nivel_usuario.data,
            nivel_numerico=form.nivel_numerico.data
        )
        user.set_password(form.password.data)
        user.set_pin(form.pin.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Usuario {user.username} creado con éxito.', 'success')
        return redirect(url_for('staff.list'))
    
    return render_template('staff/form.html', form=form, title='Nuevo Usuario de Staff')

@staff_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    user = StaffUser.query.get_or_404(id)
    
    # Solo el mismo usuario o un admin superior puede editar
    if current_user.id != user.id and current_user.nivel_numerico > 20:
        flash('No tienes permisos para editar este usuario.', 'error')
        return redirect(url_for('staff.list'))
    
    form = StaffUserForm(original_username=user.username, obj=user)
    
    if form.validate_on_submit():
        user.username = form.username.data
        user.nombres = form.nombres.data
        user.apellidos = form.apellidos.data
        user.celular_whatsapp = form.celular_whatsapp.data
        user.fecha_nacimiento = form.fecha_nacimiento.data
        user.cargo = form.cargo.data
        
        # Solo un admin puede cambiar niveles
        if current_user.nivel_numerico <= 20:
            user.nivel_usuario = form.nivel_usuario.data
            user.nivel_numerico = form.nivel_numerico.data
            
        if form.password.data:
            user.set_password(form.password.data)
        if form.pin.data:
            user.set_pin(form.pin.data)
            
        db.session.commit()
        flash(f'Usuario {user.username} actualizado.', 'success')
        return redirect(url_for('staff.list'))
    
    return render_template('staff/form.html', form=form, title='Editar Usuario', user_id=id)
