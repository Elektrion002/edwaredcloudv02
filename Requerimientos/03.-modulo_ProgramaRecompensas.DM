El objetivo es crear un subsistema capaz de administrar puntos de recompensa para clientes de negocios o tiendas, enfocado al plan de fidelidad de los clientes, debe ser capaz de administrar usuarios del staff(cajeros, administradores, usuarios), administrar clientes y sus credenciales con códigos QR, emitir credenciales de fidelidad por cliente, enviar credenciales mediante liga de portal de credenciales de cliente or wathsapp, recuperación de contraseñas y pines numéricos de acceso rápido desde el panel de mostrador.

Módulo uno app web recompensas al cliente:

crear una base de datos independiente de la master y de otros subsistemas para este módulo en el vps sobre postgresql que ya está instalado

modulo 01 Gestión de usuarios del staff
El administrador podrá agregar o editar usuarios del staff en este módulo en el sistema maestro

ID
Username
Nombres
Apellidos
celular whatsapp
Fecha nacimiento
Password
PIN Rápido 4 a 10 dígitos
Cargo
Nivel de usuario (Super Admin, Admin, User, Customer)
Nivel de usuario Numérico (10, 20, 30, 50, 100 etc)
Antigüedad
Activación lógica

Los usuarios pueden autogestionar sus contraseñas o pines dentro del mismo sistema sin importar su nivel.

Modulo 02 Gestion de Cartera de Clientes
El administrador podrá agregar o editar clientes en este módulo en el sistema maestro

ID
cliente id (alfanumérico de 10 caracteres no repetible)RFCo
Nombres
Apellidos 
celular whatsapp
Password
PIN Rápido 4-10 DÍGITOS
Dirección Física para búsqueda en mapa google
credencialID autogenerada unica irrepetible
flag de pérdida de credencial on off
Activación lógica
Los clientes pueden autogestionar sus contraseñas o pines dentro del mismo sistema sin importar su nivel.
