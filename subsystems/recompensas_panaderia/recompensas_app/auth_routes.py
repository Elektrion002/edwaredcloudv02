from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from recompensas_app import db
from recompensas_app.models.staff import StaffUser
from recompensas_app.auth_forms import StaffUnifiedLoginForm

from recompensas_app.utils.security import check_rate_limit, record_auth_fail, clear_auth_history

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = StaffUnifiedLoginForm()
    
    # Check Rate Limit
    is_allowed, info = check_rate_limit()
    if not is_allowed:
        flash(f'Demasiados intentos fallidos. Bloqueado por {info} minutos.', 'error')
        return render_template('auth/login.html', title='Acceso Bloqueado', form=form, blocked=True)
    
    if form.validate_on_submit():
        user = StaffUser.query.filter_by(username=form.username.data).first()
        if user:
            # Intentar validar como contraseña
            if user.check_password(form.secret.data):
                clear_auth_history()
                login_user(user, remember=form.remember_me.data)
                return redirect(url_for('main.index'))
            
            # Si falla como contraseña, intentar como PIN (si es numérico y 4+ dígitos)
            if form.secret.data.isdigit() and 4 <= len(form.secret.data) <= 10:
                if user.check_pin(form.secret.data):
                    clear_auth_history()
                    login_user(user, remember=form.remember_me.data)
                    return redirect(url_for('main.index'))
        
        record_auth_fail()
        flash('Credenciales inválidas (usuario, contraseña o PIN)', 'error')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/login.html', title='Iniciar Sesión', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
