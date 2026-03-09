from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from recompensas_app import db, login_manager

class StaffUser(UserMixin, db.Model):
    __tablename__ = 'staff_users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    nombres = db.Column(db.String(64), nullable=False)
    apellidos = db.Column(db.String(64), nullable=False)
    celular_whatsapp = db.Column(db.String(20), unique=True, nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=True)
    password_hash = db.Column(db.String(256), nullable=False)
    pin_hash = db.Column(db.String(256), nullable=False) # Hashed PIN (4-10 digits)
    cargo = db.Column(db.String(64), nullable=False)
    nivel_usuario = db.Column(db.String(20), default='User') # Super Admin, Admin, User
    nivel_numerico = db.Column(db.Integer, default=50) # 10, 20, 30, 50, 100
    antiguedad = db.Column(db.Date, default=datetime.utcnow)
    activo = db.Column(db.Boolean, default=True)
    
    @property
    def is_staff(self):
        return True

    @property
    def is_customer(self):
        return False

    def get_id(self):
        return f'staff_{self.id}'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def set_pin(self, pin):
        # Ensure PIN is between 4 and 10 digits as per requirement
        if len(str(pin)) >= 4 and len(str(pin)) <= 10:
            self.pin_hash = generate_password_hash(str(pin))
        else:
            raise ValueError("El PIN debe tener entre 4 y 10 dígitos.")

    def check_pin(self, pin):
        return check_password_hash(self.pin_hash, str(pin))

