from datetime import datetime
from recompensas_app import db

class Movement(db.Model):
    __tablename__ = 'movements'
    
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    
    tipo = db.Column(db.String(20), nullable=False) # 'acumulacion', 'canje', 'ajuste'
    puntos = db.Column(db.Integer, nullable=False)
    concepto = db.Column(db.String(200), nullable=False)
    
    # Saldo resultante después del movimiento para auditoría fácil
    saldo_resultante = db.Column(db.Integer, nullable=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # ID del Staff que realizó la operación (opcional para trazabilidad)
    staff_id = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f'<Movement {self.tipo}: {self.puntos} pts for Customer {self.customer_id}>'
