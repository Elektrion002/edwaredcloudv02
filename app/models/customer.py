from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class Customer(db.Model):
    __tablename__ = 'customers'
    
    id = db.Column(db.Integer, primary_key=True)
    codigo_unico = db.Column(db.String(20), unique=True, index=True) # CF00000001
    rfc = db.Column(db.String(20), unique=True, index=True)
    nombre_negocio = db.Column(db.String(150), nullable=False)
    nombres = db.Column(db.String(100))
    apellidos = db.Column(db.String(100))
    whatsapp = db.Column(db.String(20))
    password_hash = db.Column(db.String(256))
    pin_rapido = db.Column(db.String(10)) # 4 to 10 digits
    direccion = db.Column(db.Text) # For Google Maps
    ruta_asignada = db.Column(db.String(100))
    vendedor_asignado = db.Column(db.String(100))
    credito_asignado = db.Column(db.Numeric(10, 2), default=0.0)
    deuda_acumulada = db.Column(db.Numeric(10, 2), default=0.0)
    
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    activo = db.Column(db.Boolean, default=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<Customer {self.nombre_negocio}>'
