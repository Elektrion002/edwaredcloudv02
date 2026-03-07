from datetime import datetime
import secrets
from recompensas_app import db
from werkzeug.security import generate_password_hash, check_password_hash

class Customer(db.Model):
    __tablename__ = 'customers'
    
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.String(10), unique=True, nullable=False, index=True) # EDW-XXXXXX
    nombres = db.Column(db.String(100), nullable=False)
    apellidos = db.Column(db.String(100), nullable=False)
    celular_whatsapp = db.Column(db.String(20), unique=True, nullable=False)
    direccion_fisica = db.Column(db.Text, nullable=True) # Para búsqueda en Google Maps
    
    password_hash = db.Column(db.String(255), nullable=True)
    pin_hash = db.Column(db.String(255), nullable=True) # 4-10 dígitos
    
    credencial_id = db.Column(db.String(64), unique=True, nullable=False, index=True) # Token para QR
    flag_perdida = db.Column(db.Boolean, default=False)
    
    puntos_disponibles = db.Column(db.Integer, default=0)
    puntos_canjeados = db.Column(db.Integer, default=0)
    
    activo = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relación con movimientos
    movements = db.relationship('Movement', backref='customer', lazy='dynamic', cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def set_pin(self, pin):
        # Validar 4-10 dígitos
        if len(str(pin)) >= 4 and len(str(pin)) <= 10:
            self.pin_hash = generate_password_hash(str(pin))
        else:
            raise ValueError("El PIN debe tener entre 4 y 10 dígitos.")

    def check_pin(self, pin):
        return check_password_hash(self.pin_hash, str(pin))

    @staticmethod
    def generate_credencial_id():
        return secrets.token_urlsafe(32)

    def __repr__(self):
        return f'<Customer {self.cliente_id} - {self.nombres}>'
