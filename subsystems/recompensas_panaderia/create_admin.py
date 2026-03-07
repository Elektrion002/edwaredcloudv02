import sys
import os

# Ajustar PYTHONPATH para encontrar el paquete recompensas_app
sys.path.append('/var/www/edwared_cloud_v2/subsystems/recompensas_panaderia')

from recompensas_app import create_app, db
from recompensas_app.models.staff import StaffUser

app = create_app()
with app.app_context():
    # Verificar si el usuario ya existe
    user = StaffUser.query.filter_by(username='admin_temp').first()
    if not user:
        user = StaffUser(
            username='admin_temp',
            nombres='Admin',
            apellidos='Temporal',
            celular_whatsapp='520000000000',
            cargo='Soporte',
            nivel_usuario='Super Admin',
            nivel_numerico=10
        )
        user.set_password('MEwar3x4-12VpS')
        user.set_pin('1234')
        db.session.add(user)
        db.session.commit()
        print("Usuario admin_temp creado exitosamente.")
    else:
        print("El usuario admin_temp ya existe.")
