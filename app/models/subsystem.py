from app import db
from datetime import datetime

class Subsystem(db.Model):
    __tablename__ = 'subsystems'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    ruta = db.Column(db.String(200), nullable=False, unique=True) # ej: /rpandemo01
    db_nombre = db.Column(db.String(100), nullable=True)
    
    # Credenciales administrativas vinculadas (Relación con Cliente)
    cliente_admin_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=True)
    admin_password = db.Column(db.String(200), nullable=True)
    
    puerto = db.Column(db.Integer, nullable=False)
    tipo = db.Column(db.String(50), default='web') # web, api, etc.
    descripcion = db.Column(db.Text, nullable=True)
    activo = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relación para acceder al objeto cliente fácilmente
    cliente_admin = db.relationship('Customer', backref='managed_subsystems')

    def __repr__(self):
        return f'<Subsystem {self.nombre} ({self.ruta})>'
