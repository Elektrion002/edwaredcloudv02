from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from app import db
from app.models.staff import StaffUser
from app.auth_forms import StaffLoginForm, QuickPinLoginForm

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = StaffLoginForm()
    pin_form = QuickPinLoginForm()
    
    if form.validate_on_submit():
        user = StaffUser.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Usuario o contraseña inválidos', 'error')
            return redirect(url_for('auth.login'))
        
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('main.index'))
    
    return render_template('auth/login.html', title='Iniciar Sesión', form=form, pin_form=pin_form)

@bp.route('/login-pin', methods=['POST'])
def login_pin():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = QuickPinLoginForm()
    if form.validate_on_submit():
        user = StaffUser.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_pin(form.pin.data):
            flash('Usuario o PIN inválidos', 'error')
            return redirect(url_for('auth.login'))
        
        login_user(user)
        return redirect(url_for('main.index'))
    
    return redirect(url_for('auth.login'))

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
