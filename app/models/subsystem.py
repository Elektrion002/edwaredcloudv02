from app import db
from datetime import datetime

class Subsystem(db.Model):
    __tablename__ = 'subsystems'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    ruta = db.Column(db.String(255), nullable=False)
    db_name = db.Column(db.String(100))
    
    # Relación con el Cliente (Dueño del subsistema)
    usuario_admin_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    
    password_admin = db.Column(db.String(256)) # Enmascarada/Encriptada si es necesario
    puerto = db.Column(db.Integer)
    tipo = db.Column(db.String(50), default='web') # web, api, etc.
    descripcion = db.Column(db.Text)
    
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    activo = db.Column(db.Boolean, default=True)
    
    # Relationship back to Customer
    admin_cliente = db.relationship('Customer', backref=db.backref('subsystems', lazy=True))

    def __repr__(self):
        return f'<Subsystem {self.nombre}>'
