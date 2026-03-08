from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from werkzeug.middleware.proxy_fix import ProxyFix

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

    db.init_app(app)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        if user_id.startswith('staff_'):
            from recompensas_app.models.staff import StaffUser
            return StaffUser.query.get(int(user_id.split('_')[1]))
        elif user_id.startswith('cust_'):
            from recompensas_app.models.customer import Customer
            return Customer.query.get(int(user_id.split('_')[1]))
        return None

    # Register blueprints
    from recompensas_app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from recompensas_app.auth_routes import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from recompensas_app.staff_routes import staff_bp
    app.register_blueprint(staff_bp, url_prefix='/admin/staff')

    from recompensas_app.customer_routes import bp as customer_bp
    app.register_blueprint(customer_bp)

    from recompensas_app.counter_routes import bp as counter_bp
    app.register_blueprint(counter_bp)

    from recompensas_app.portal_routes import portal_bp
    app.register_blueprint(portal_bp)

    with app.app_context():
        from recompensas_app.models import staff, customer, movement
        db.create_all()

    return app
