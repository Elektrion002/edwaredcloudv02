from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class StaffUser(UserMixin, db.Model):
    __tablename__ = 'staff_users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    nombres = db.Column(db.String(100), nullable=False)
    apellidos = db.Column(db.String(100), nullable=False)
    whatsapp = db.Column(db.String(20))
    fecha_nacimiento = db.Column(db.Date)
    password_hash = db.Column(db.String(256))
    pin_rapido = db.Column(db.String(10)) # 4 to 10 digits
    cargo = db.Column(db.String(100))
    
    # Nivel de usuario (Labels: Super Admin, Admin, User, Customer)
    nivel_etiqueta = db.Column(db.String(50), default='User')
    # Nivel de usuario Numerico (10, 20, 30, 50, 100 etc)
    nivel_numerico = db.Column(db.Integer, default=50)
    
    antiguedad = db.Column(db.DateTime, default=datetime.utcnow)
    activo = db.Column(db.Boolean, default=True)
    
    @property
    def is_staff(self):
        return True
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def set_pin(self, pin):
        # Additional validation could be added here
        self.pin_rapido = pin

@login_manager.user_loader
def load_user(id):
    from flask import session
    from app.models.customer import Customer
    
    user_type = session.get('user_type')
    if user_type == 'customer':
        return Customer.query.get(int(id))
    return StaffUser.query.get(int(id))
