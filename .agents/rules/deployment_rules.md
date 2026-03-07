# Reglas de Despliegue de Subsistemas (Fase 05+)

Esta regla define los estándares técnicos obligatorios para la creación y despliegue de nuevos subsistemas o microservicios en el VPS, con el fin de garantizar el aislamiento, la integridad y el correcto enrutamiento.

## 1. Identidad y Aislamiento de Código

- **Nombramiento Único**: Nunca usar nombres genéricos como `app` para la carpeta principal del subsistema. Cada subsistema debe tener un nombre de paquete único y descriptivo (ej: `recompensas_app`, `catalogos_app`).
- **Importaciones**: Todas las referencias internas deben usar el nombre del paquete único para evitar colisiones con el sistema maestro u otros módulos.
- **Punto de Entrada**: El archivo `run.py` debe estar en la raíz de la carpeta del subsistema y apuntar correctamente al objeto `app` del paquete renombrado.

## 2. Configuración de Red y Proxy

- **Puertos**: Cada subsistema debe operar en un puerto único (ej: 5001, 5002...).
- **ProxyFix**: Es obligatorio activar el middleware `ProxyFix` de Werkzeug en la inicialización de Flask para manejar correctamente el enrutamiento detrás de Nginx:
  ```python
  from werkzeug.middleware.proxy_fix import ProxyFix
  app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)
  ```
- **Nginx Headers**: La configuración de Nginx en `/etc/nginx/sites-available/edwared_cloud` debe incluir siempre el encabezado `X-Forwarded-Prefix`:
  ```nginx
  location /nombre_subsistema/ {
      include proxy_params;
      proxy_pass http://localhost:PORT/;
      proxy_set_header X-Forwarded-Prefix /nombre_subsistema;
  }
  ```

## 3. Integridad del Despliegue

- **Prohibido Inyectar Código vía SSH**: No se deben usar comandos `ssh` directos para escribir archivos de configuración complejos (riesgo de corrupción por interpolación de variables en el shell).
- **Uso de SCP**: Siempre preparar archivos de configuración (`.service`, Nginx configs) localmente y subirlos mediante `scp` al VPS.
- **Gestión de Procesos**: Antes de reiniciar un servicio que haya fallado, limpiar procesos huérfanos con `pkill -f gunicorn` si el puerto permanece bloqueado.

---

> [!IMPORTANT]
> Consultar siempre el archivo `analis_fallos.md` local para más detalles históricos sobre la resolución de problemas específicos.
