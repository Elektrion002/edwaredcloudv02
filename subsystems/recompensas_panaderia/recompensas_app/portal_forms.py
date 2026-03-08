from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, Optional
from recompensas_app.models.customer import Customer

class CustomerPortalLoginForm(FlaskForm):
    cliente_id = StringField('ID de Credencial', validators=[DataRequired(), Length(min=10, max=10)])
    secret = PasswordField('Password o PIN', validators=[DataRequired()])
    remember_me = BooleanField('Recordarme')
    submit = SubmitField('ENTRAR A MI PORTAL')

class CustomerUpdateSecretForm(FlaskForm):
    current_secret = PasswordField('Clave o PIN Actual', validators=[DataRequired()])
    new_password = PasswordField('Nueva Contraseña (Opcional)', validators=[
        Optional(), 
        Length(min=6, message='La contraseña debe tener al menos 6 caracteres')
    ])
    new_pin = PasswordField('Nuevo PIN 4-10 Dígitos (Opcional)', validators=[
        Optional(), 
        Length(min=4, max=10, message='El PIN debe tener entre 4 y 10 dígitos')
    ])
    confirm_secret = PasswordField('Confirmar Nueva Clave/PIN', validators=[
        EqualTo('new_password', message='Las contraseñas no coinciden')
    ])
    submit = SubmitField('ACTUALIZAR SEGURIDAD')

    def validate_new_pin(self, field):
        if field.data:
            pin = field.data
            # Lista negra de PINs triviales
            weak_pins = [
                '0000', '1111', '2222', '3333', '4444', '5555', '6666', '7774', '8888', '9999',
                '1234', '4321', '2580'
            ]
            if pin in weak_pins:
                raise ValidationError('Este PIN es demasiado común y no es seguro. Por favor elige otro.')
            if not pin.isdigit():
                raise ValidationError('El PIN debe contener solo números.')

    def validate_new_password(self, field):
        if field.data:
            password = field.data
            # Verificar si es demasiado simple (ej. solo números o solo letras)
            if password.isdigit() or password.isalpha():
                raise ValidationError('La contraseña debe ser más compleja (combina letras y números).')

class CustomerRecoveryForm(FlaskForm):
    celular_whatsapp = StringField('Número de WhatsApp Registrado', validators=[DataRequired()])
    submit = SubmitField('SOLICITAR RECUPERACIÓN')
