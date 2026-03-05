from flask import render_template
from app.admin import bp

@bp.route('/login')
def login():
    return render_template('admin/login.html', title='Admin Login')
