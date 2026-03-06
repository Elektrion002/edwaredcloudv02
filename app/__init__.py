from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'admin.login'

from flask_login import AnonymousUserMixin
class AnonymousUser(AnonymousUserMixin):
    is_staff = False

login_manager.anonymous_user = AnonymousUser

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)

    # Register blueprints here
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.admin import bp as admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')

    with app.app_context():
        from app.models import user, customer
        db.create_all()

    return app
