from recompensas_app import create_app, db
from recompensas_app.models.staff import StaffUser
from datetime import date

app = create_app()

def init_db():
    with app.app_context():
        # Clean and create tables
        db.create_all()
        
        # Check if super admin exists
        admin = StaffUser.query.filter_by(username='edwared001').first()
        if not admin:
            admin = StaffUser(
                username='edwared001',
                nombres='Admin',
                apellidos='Maestro',
                celular_whatsapp='0000000000',
                fecha_nacimiento=date(1990, 1, 1),
                cargo='Super Administrador',
                nivel_usuario='Super Admin',
                nivel_numerico=10,
                activo=True
            )
            admin.set_password('0686')
            admin.set_pin('0686')
            db.session.add(admin)
            db.session.commit()
            print("Usuario edwared001 creado (Pass: 0686, PIN: 0686)")
        else:
            print("El usuario ya existe.")

if __name__ == '__main__':
    init_db()
