from recompensas_app import db
from datetime import datetime

class Product(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.String(50), unique=True, nullable=False, index=True)
    descripcion = db.Column(db.String(255), nullable=False)
    tipo_producto = db.Column(db.String(100))
    
    # Precios
    precio_venta = db.Column(db.Float, default=0.0)
    precio_costo = db.Column(db.Float, default=0.0) # Dato sensible (solo Staff)
    
    # Sistema de Puntos
    precio_puntos = db.Column(db.Integer, default=0) # Puntos requeridos para canje
    es_canjeable = db.Column(db.Boolean, default=False)
    puntos_generados = db.Column(db.Integer, default=0) # Puntos ganados por compra
    
    # Gestión de Medios y Estado
    imagen_path = db.Column(db.String(255))
    activo = db.Column(db.Boolean, default=True) # Desactivado lógico
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Product {self.sku} - {self.descripcion}>'

    def to_dict(self):
        return {
            'id': self.id,
            'sku': self.sku,
            'descripcion': self.descripcion,
            'tipo_producto': self.tipo_producto,
            'precio_venta': self.precio_venta,
            'precio_puntos': self.precio_puntos,
            'es_canjeable': self.es_canjeable,
            'puntos_generados': self.puntos_generados,
            'imagen_path': self.imagen_path,
            'activo': self.activo
        }
