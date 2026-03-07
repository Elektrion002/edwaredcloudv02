# 🧠 Lecciones Aprendidas: Despliegue de Subsistemas (Fase 05)

Este documento sirve como guía técnica para el despliegue de microservicios en el VPS, basado en los retos superados durante la implementación del **Subsistema 01 (Recompensas Panadería)**.

---

## 1. Conflictos de Identidad (Aislamiento de Paquetes)

> [!IMPORTANT]
> **Error Detectado**: Ambos proyectos (Maestro y Subsistema) usaban el nombre de carpeta genérico `app/`. Al ejecutar Gunicorn en una estructura compartida, Python priorizaba el paquete `app` de la raíz (Sistema Maestro), ignorando el local.
>
> **Solución Aplicada**: Renombrar el paquete principal de cada subsistema con un nombre descriptivo único (ej: `recompensas_app`).

---

## 2. Enrutamiento en Subdirectorios (Proxy Pass)

> [!TIP]
> **Error Detectado**: Al servir el subsistema en una ruta como `/rpandemo01/`, las funciones `url_for` de Flask generaban enlaces que omitían el prefijo.
>
> **Solución Aplicada**:
>
> 1. Implementar el middleware `ProxyFix` de Werkzeug.
> 2. Configurar Nginx para enviar el encabezado `X-Forwarded-Prefix /rpandemo01;`.

---

## 3. Integridad de Configuración (PowerShell vs SSH)

> [!CAUTION]
> **Error Detectado**: El uso de comandos `ssh` directos desde PowerShell para escribir configuraciones causaba corrupción por expansión de variables (ej: `$host`).
>
> **Solución Aplicada**: Preparar archivos localmente y subirlos íntegramente mediante `scp`.

---

## 4. Gestión de Puertos y Procesos Residuales

> [!NOTE]
> **Error Detectado**: Procesos huérfanos de Gunicorn bloqueando el puerto **5001**.
>
> **Solución Aplicada**: Limpieza preventiva con `pkill -f gunicorn` y uso de servicios `systemd` con `Restart=always`.

---

## ✅ Resumen Preventivo

1. **Nombre Único**: Paquete de app específico.
2. **Middleware**: `ProxyFix` obligatorio.
3. **Despliegue**: Solo vía `scp`.
4. **Proxy**: Header `X-Forwarded-Prefix` en Nginx.
