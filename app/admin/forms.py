from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, DateField, BooleanField
from wtforms.validators import DataRequired, Length, Optional, EqualTo

class StaffUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=64)])
    nombres = StringField('Nombres', validators=[DataRequired(), Length(max=100)])
    apellidos = StringField('Apellidos', validators=[DataRequired(), Length(max=100)])
    whatsapp = StringField('WhatsApp/Celular', validators=[Optional(), Length(max=20)])
    fecha_nacimiento = DateField('Fecha de Nacimiento', format='%Y-%m-%d', validators=[Optional()])
    password = PasswordField('Contraseña', validators=[Optional(), Length(min=6, max=128)])
    confirm_password = PasswordField('Confirmar Contraseña', validators=[EqualTo('password')])
    pin_rapido = StringField('PIN Rápido (4-10 dígitos)', validators=[Optional(), Length(min=4, max=10)])
    cargo = StringField('Cargo', validators=[Optional(), Length(max=100)])
    
    nivel_etiqueta = SelectField('Nivel de Acceso', choices=[
        ('Super Admin', 'Super Admin'),
        ('Admin', 'Admin'),
        ('User', 'User'),
        ('Customer', 'Customer')
    ], default='User')
    
    nivel_numerico = SelectField('Nivel Numérico', choices=[
        ('10', '10 (Super Admin)'),
        ('20', '20 (Admin)'),
        ('50', '50 (User)'),
        ('100', '100 (Customer)')
    ], default='50')
    
    activo = BooleanField('Activo', default=True)
    submit = SubmitField('Guardar Usuario')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Recordarme')
    submit = SubmitField('Iniciar Sesión')
