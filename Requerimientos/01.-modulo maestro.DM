
Objetivo es crear una app web maestra que pueda albergar subsistemas en un vps programada en python con flask htmls js y css talves svg,

la app web master podra gestionar desde su panel principal la redirección de los subsistemas con tarjetas, este debe ser responsivo actual y debe establecer reglas de diseño para que todo subsistema tenga solo sutiles cambios, fuentes areales usos de temas con azul medianoche con contrastes de casi blancos en los caracteres, tarjetas con colores minimalistas y de buen contraste en las fuentes, todo responsivo, si se usa una base esta no debe estorbar o desbordarse cuando se use un teléfono celular o tablet, menus de hamburguesa. debe garantizarse la separación de sub app webs del principal.

Fase 01
usar git ssh git@github.com:Elektrion002/edwaredcloudv02.git
Get started by creating a new file or uploading an existing file. We recommend every repository include a README, LICENSE, and .gitignore.

echo "# edwaredcloudv02" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin git@github.com:Elektrion002/edwaredcloudv02.git
git push -u origin main

git remote add origin git@github.com:Elektrion002/edwaredcloudv02.git
git branch -M main
git push -u origin main

crear entorno virtual venv de todo el sistema general maestro.
crear folders de acuerdo a la buenas practicas de modularidad blue prints etc.
mantener 5s en el codigo y en los archivos.

Crear un dashboard de bienvenida al sistema el cual será responsivo, en él pondremos tarjetas con las descripciones de cada módulo del sistema maestro que nos lleva a los subsistemas en sus rutas. también tiene un botón de login pequeño no invasivo para administrar el sistema principal y una ruta específica para ello aislado totalmente, 

Fase 02
instalar posgresql en el vps
ssh root@187.124.81.209
MEwar3x4-12VpS
root

Crear una base de datos en el VPS con posgreSQL y hacer un tunel para auditarla desde la pc local
emitir los parametros ssh y datos que pide para conexion desde pgAdmin4


Respuesta fue la siguiente 

Parámetros para pgAdmin4 (Vía Túnel SSH):
Para conectarte desde tu PC local usando pgAdmin4, utiliza los siguientes datos:

1. Pestaña "SSH Tunnel":

Tunnel host: 187.124.81.209
SSH Port: 22
Username: root
Authentication: Password
Password: MEwar3x4-12VpS
2. Pestaña "Connection":

Host name/address: localhost (El túnel lo redirigirá)
Port: 5432
Maintenance database: edwared_master
Username: edwared_admin
Password: MEwar3x4-12VpS

Fase 03

modulo 01 Gestión de usuarios del staff
El administrador podrá agregar o editar usuarios del staff en este módulo en el sistema maestro. este debe estar oculto del panel principal de bienvenida publico, el panel publico tiene las taregtas de los microservicios web que tiene el sistema maestro llamados subsistemas, el panel del administrador permite la gestion de usuarios y es distinto al publico para acceder a el es necesario el login al sistema maestro y su base de datos es independiente de los subsistemas aqui los items de la base de datos de usuarios de sistema maestro:

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
nos e deben mostrar datos sencibles en ningun formulario de gestion de usuarios delñ estaff en el modulo maestro, tomarlo como leecion aprendida para subsistemas o microservicios


FASE 04
Modulo 02 Gestion de Cartera de Clientes sistema maestro


El administrador podrá agregar o editar clientes en este módulo en el sistema maestro


ID
Código Único 10 caracteres (CF00000001)
RFC
Nombre de Negocio
Nombres (Representante si es una empresa)
Apellidos (Representante si es una empresa)
celular whatsapp
Password
PIN Rápido 4-10 DÍGITOS
Dirección Física para búsqueda en mapa google
Ruta Asignada
Vendedor Asignado
Crédito asignado
Deuda Acumulada
Activación lógica

El cliente puede autogestionar su password y contraseña en la ruta de clientes. los datos sensibles no deben verse en ningun formulario.

Modulo 03
El administrador podrá agregar o editar items de la tabla de subsistemas o microservicios del modulo maestro

crear la tabla de subsistemas o microservicios en la db del sistema maestro
ID
Nombre del subsistema
Ruta del subsistema
DB del subsistema
Usuario admin del subsistema FkID Clientes
Password admin del subsistema FkID Clientes password
Puerto del subsistema
tipo del susbsistema (web, api, etc)
Descripción del subsistema
Activación lógica