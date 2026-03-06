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
no mostrar informacion sensible como pines y contraseñas, evaluar simepre antes de sumitir un cambio, 
enviar mensajes de error en lugar de matar la pagina

Modulo 02 Gestion de Cartera de Clientes
El administrador podrá agregar o editar clientes en este módulo en el sistema maestro

ID
cliente id (alfanumérico de 10 caracteres no repetible)
Nombres
Apellidos 
celular whatsapp
Password
PIN Rápido 4-10 DÍGITOS
Dirección Física para búsqueda en mapa google
credencialID autogenerada unica irrepetible se usara para generar el codigo QR de la credencial.
flag de pérdida de credencial on off
puntos disponibles
puntos canjeados
Activación lógica
Los clientes pueden autogestionar sus contraseñas o pines dentro del mismo sistema sin importar su nivel.

si el cliente se olvida de su pin o contraseña podra autogestionar enviando por whats app
una temporal desde el mismo subsistema usando su numero celular
el cajero o administrador podra enviar la ruta de credenciales a los clientes
ellos podran acceder a su credencial con un login dependiente de sus datos al hacer login en la ruta con su identificador pin o contraseña podra ver su codigo QR
el cliente podra ver sus ultimos movimientos o solicitar un reporte de los mismos como en el banco.


Modulo 03 Gestión de Puntos de Recompensa
El cajero o usuarios del staff del subsistema o microservicio agregar o canjear puntos de recompensa 
en este módulo en el subsistema o microservicio

al hacer login en este modulo el personal del estaff del subisitema o microservisio sera guiado 
a un panel de cange de puntos y tendra disponibles las siguientes caracteristicas:

Campo de escanneo de la credencial mediente QR del usuario
Campo de busqueda por numero telefonico del cliente o codigo de la credencial
campo de asignar agregar puntos o cangear puntos al cliente podria abrirse un modal para ello
Boton de registro de clientes te redigira a la gestion de clientes agregar nuevo

modulo 04
el administrador del subsistema podra tener accesos a los modulos de administracion de usuarios del staff y clientes asi como de paneles de estadisticas y tablas cardex del subsitema
panel de estadisticas aqui aparecen las graficas de los top y kpi de los canges que se hacen
top de cleintes puntos generados
tops clientes que cambian puntos
top de usuarios que asignan puntos
top de usuarios que congean puntos
tablas de cardex por tiempo hoy ayer semana Historico o tiempo definido por el usuarios
filtros de cardex o busquedas en la tabla cardex
targetas tipo kpi representando dinero cangeado compras que generan puntos.

modulo 05
Catalogo de productos 

el subsistema o microservicio tendra una tabla donde gestionenen el catalogo de productos para saber cuantos puntos genera la compra d eun producto 
y que cantidad de puntos se requieren para cangear alguno de ellos

ID
SKU
descripcion
tipo de producto
Precio de venta
precio costo
precio en puntos cangeables
bandera de si es cangeable o no con puntos recompensas
puntos que genera su compra
imagen se debe guardar en una carpeta en el vps
desactivado logico

validar sku unicos y datos que sean obligatorios deben ser evaluados para no tirar la pagina al editar o crear
datos sensibles no deben 







