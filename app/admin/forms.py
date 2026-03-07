from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, DateField, BooleanField
from wtforms.validators import DataRequired, Length, Optional, EqualTo, ValidationError

class StaffUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=64)])
    nombres = StringField('Nombres', validators=[DataRequired(), Length(max=100)])
    apellidos = StringField('Apellidos', validators=[DataRequired(), Length(max=100)])
    whatsapp = StringField('WhatsApp/Celular', validators=[Optional(), Length(max=20)])
    fecha_nacimiento = DateField('Fecha de Nacimiento', format='%Y-%m-%d', validators=[Optional()])
    password = PasswordField('Contraseña', validators=[Optional(), Length(min=6, max=128)])
    confirm_password = PasswordField('Confirmar Contraseña', validators=[EqualTo('password')])
    pin_rapido = PasswordField('PIN Rápido (4-10 dígitos)', validators=[Optional(), Length(min=4, max=10)])
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

class CustomerForm(FlaskForm):
    codigo_unico = StringField('Código Único (CF00000001) *', validators=[DataRequired('El código único es obligatorio'), Length(max=20)])
    rfc = StringField('RFC *', validators=[DataRequired('El RFC es obligatorio'), Length(max=20)])
    nombre_negocio = StringField('Nombre de Negocio', validators=[DataRequired(), Length(max=150)])
    nombres = StringField('Nombres (Representante)', validators=[Optional(), Length(max=100)])
    apellidos = StringField('Apellidos (Representante)', validators=[Optional(), Length(max=100)])
    whatsapp = StringField('WhatsApp/Celular', validators=[Optional(), Length(max=20)])
    password = PasswordField('Password', validators=[Optional(), Length(min=6, max=128)])
    pin_rapido = PasswordField('PIN Rápido (4-10 dígitos)', validators=[Optional(), Length(min=4, max=10)])
    direccion = StringField('Dirección Física (Google Maps)', validators=[Optional()])
    ruta_asignada = StringField('Ruta Asignada', validators=[Optional()])
    vendedor_asignado = StringField('Vendedor Asignado', validators=[Optional()])
    credito_asignado = StringField('Crédito Asignado', validators=[Optional()])
    deuda_acumulada = StringField('Deuda Acumulada', validators=[Optional()])
    activo = BooleanField('Activo', default=True)
    submit = SubmitField('Guardar Cliente')

    def __init__(self, *args, **kwargs):
        self.original_id = kwargs.get('obj').id if kwargs.get('obj') else None
        super(CustomerForm, self).__init__(*args, **kwargs)

    def validate_codigo_unico(self, codigo_unico):
        from app.models.customer import Customer
        customer = Customer.query.filter_by(codigo_unico=codigo_unico.data).first()
        if customer and (self.original_id is None or customer.id != self.original_id):
            raise ValidationError('Este Código Único ya está registrado en otro cliente.')

    def validate_rfc(self, rfc):
        from app.models.customer import Customer
        customer = Customer.query.filter_by(rfc=rfc.data).first()

class CustomerLoginForm(FlaskForm):
    codigo_unico = StringField('Código Único', validators=[DataRequired()])
    password = PasswordField('Password / PIN', validators=[DataRequired()])
    remember_me = BooleanField('Recordarme')
    submit = SubmitField('Iniciar Sesión Cliente')

class ForgotPasswordForm(FlaskForm):
    whatsapp = StringField('Número de WhatsApp/Celular', validators=[DataRequired(), Length(max=20)])
    submit = SubmitField('Recuperar Acceso')

class SubsystemForm(FlaskForm):
    nombre = StringField('Nombre del Subsistema *', validators=[DataRequired(), Length(max=100)])
    ruta = StringField('Ruta / Dominio *', validators=[DataRequired(), Length(max=200)])
    db_nombre = StringField('Nombre de BD', validators=[Optional(), Length(max=100)])
    
    # Campo para seleccionar el Cliente responsable
    cliente_admin_id = SelectField('Cliente Administrador *', coerce=int, validators=[DataRequired()])
    
    admin_password = PasswordField('Password Admin Subsistema', validators=[Optional(), Length(max=200)])
    puerto = StringField('Puerto', validators=[DataRequired()])
    
    tipo = SelectField('Tipo de Subsistema', choices=[
        ('web', 'Web Application'),
        ('api', 'API Service'),
        ('microservice', 'Microservice'),
        ('database', 'Database Service')
    ], default='web')
    
    descripcion = StringField('Descripción', validators=[Optional()])
    activo = BooleanField('Activo', default=True)
    submit = SubmitField('Guardar Subsistema')

    def __init__(self, *args, **kwargs):
        super(SubsystemForm, self).__init__(*args, **kwargs)
        from app.models.customer import Customer
        # Cargar clientes activos para el selector
        try:
            self.cliente_admin_id.choices = [(c.id, f"{c.codigo_unico} - {c.nombre_negocio}") 
                                           for c in Customer.query.filter_by(activo=True).all()]
        except Exception:
            self.cliente_admin_id.choices = []
