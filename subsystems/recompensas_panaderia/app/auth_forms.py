from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, DateField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, Optional
from app.models.staff import StaffUser

class StaffLoginForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    remember_me = BooleanField('Recordarme')
    submit = SubmitField('Iniciar Sesión')

class QuickPinLoginForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired()])
    pin = PasswordField('PIN Rápido', validators=[DataRequired(), Length(min=4, max=10)])
    submit = SubmitField('Entrar con PIN')

class StaffUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=64)])
    nombres = StringField('Nombres', validators=[DataRequired()])
    apellidos = StringField('Apellidos', validators=[DataRequired()])
    celular_whatsapp = StringField('WhatsApp', validators=[DataRequired()])
    fecha_nacimiento = DateField('Fecha Nacimiento', validators=[Optional()])
    cargo = StringField('Cargo', validators=[DataRequired()])
    nivel_usuario = SelectField('Nivel de Acceso', choices=[
        ('Super Admin', 'Super Admin'),
        ('Admin', 'Admin'),
        ('User', 'User')
    ], default='User')
    nivel_numerico = SelectField('Prioridad', choices=[
        (10, '10 - Dueño'),
        (20, '20 - Gerente'),
        (50, '50 - Cajero/Vendedor'),
        (100, '100 - Soporte Externo')
    ], coerce=int, default=50)
    password = PasswordField('Contraseña', validators=[Optional(), Length(min=6)])
    pin = PasswordField('PIN Rápido (4-10 dígitos)', validators=[Optional(), Length(min=4, max=10)])
    submit = SubmitField('Guardar Usuario')

    def __init__(self, original_username=None, *args, **kwargs):
        super(StaffUserForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = StaffUser.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Este nombre de usuario ya está registrado.')
