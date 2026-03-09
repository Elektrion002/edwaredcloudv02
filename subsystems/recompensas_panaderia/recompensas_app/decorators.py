from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user

def staff_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not hasattr(current_user, 'username'):
            flash('Acceso denegado. Esta sección es solo para personal autorizado.', 'error')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not hasattr(current_user, 'username') or current_user.nivel_numerico > 30:
            flash('No tienes permisos administrativos para acceder a esta sección.', 'error')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function
