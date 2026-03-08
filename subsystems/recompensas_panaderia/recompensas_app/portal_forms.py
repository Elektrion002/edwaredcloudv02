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
    new_password = PasswordField('Nueva Contraseña (Opcional)', validators=[Optional(), Length(min=6)])
    new_pin = PasswordField('Nuevo PIN 4-10 Dígitos (Opcional)', validators=[Optional(), Length(min=4, max=10)])
    confirm_secret = PasswordField('Confirmar Nueva Clave/PIN', validators=[
        EqualTo('new_password', message='Las contraseñas no coinciden')
    ])
    submit = SubmitField('ACTUALIZAR SEGURIDAD')

class CustomerRecoveryForm(FlaskForm):
    celular_whatsapp = StringField('Número de WhatsApp Registrado', validators=[DataRequired()])
    submit = SubmitField('SOLICITAR RECUPERACIÓN')
