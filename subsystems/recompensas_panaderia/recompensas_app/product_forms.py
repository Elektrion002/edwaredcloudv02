from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FloatField, IntegerField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from recompensas_app.models.product import Product

class ProductForm(FlaskForm):
    sku = StringField('SKU', validators=[DataRequired(), Length(min=2, max=50)])
    descripcion = StringField('Descripción', validators=[DataRequired(), Length(max=255)])
    tipo_producto = StringField('Categoría / Tipo', validators=[Length(max=100)])
    
    precio_venta = FloatField('Precio de Venta ($)', default=0.0)
    precio_costo = FloatField('Precio de Costo ($)', default=0.0)
    
    precio_puntos = IntegerField('Precio en Puntos (Canje)', default=0)
    es_canjeable = BooleanField('¿Es Canjeable con Puntos?')
    puntos_generados = IntegerField('Puntos que Genera la Compra', default=0)
    
    activo = BooleanField('Producto Activo', default=True)
    submit = SubmitField('Guardar Producto')

    def __init__(self, original_sku=None, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.original_sku = original_sku

    def validate_sku(self, sku):
        if sku.data != self.original_sku:
            product = Product.query.filter_by(sku=sku.data).first()
            if product:
                raise ValidationError('Este SKU ya está registrado. Debe ser único.')
