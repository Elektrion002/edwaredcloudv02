from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, ValidationError, Optional
from recompensas_app.models.customer import Customer

class CustomerForm(FlaskForm):
    cliente_id = StringField('ID Cliente (10 caracteres)', validators=[DataRequired(), Length(min=10, max=10)])
    nombres = StringField('Nombres', validators=[DataRequired()])
    apellidos = StringField('Apellidos', validators=[DataRequired()])
    celular_whatsapp = StringField('WhatsApp', validators=[DataRequired()])
    direccion_fisica = TextAreaField('Dirección Física (Mapa)', validators=[Optional()])
    
    password = PasswordField('Contraseña (Hacer clic en ojo para ver)', validators=[Optional(), Length(min=6)])
    pin = PasswordField('PIN Rápido (4-10 dígitos)', validators=[Optional(), Length(min=4, max=10)])
    
    activo = BooleanField('Cliente Activo', default=True)
    submit = SubmitField('Guardar Cliente')

    def __init__(self, original_cliente_id=None, original_whatsapp=None, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)
        self.original_cliente_id = original_cliente_id
        self.original_whatsapp = original_whatsapp

    def validate_cliente_id(self, cliente_id):
        if cliente_id.data != self.original_cliente_id:
            customer = Customer.query.filter_by(cliente_id=cliente_id.data).first()
            if customer is not None:
                raise ValidationError('Este ID de cliente ya está registrado.')

    def validate_celular_whatsapp(self, celular_whatsapp):
        if celular_whatsapp.data != self.original_whatsapp:
            customer = Customer.query.filter_by(celular_whatsapp=celular_whatsapp.data).first()
            if customer is not None:
                raise ValidationError('Este número de WhatsApp ya está registrado.')
