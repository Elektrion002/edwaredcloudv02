# Lecciones Aprendidas: Módulo 02 - Gestión de Clientes (Fase 05)

Este documento resume los desafíos técnicos y las soluciones implementadas durante el desarrollo del sistema de fidelización del Subsistema 01.

## 1. Conectividad y Puertos (El Error Sistémico)

> [!IMPORTANT]
> **Error**: Tanto el Subsistema como el Maestro intentaban conectar a PostgreSQL por el puerto `5433`, pero la base de datos en el VPS estaba activa en el puerto estándar `5432`.
>
> **Lección**: Siempre verificar el puerto real de escucha del servicio en el VPS (`netstat -tuln`) antes de configurar las cadenas de conexión. No asumir puertos no estándar.
>
> **Solución**: Unificamos todos los servicios a `localhost:5432`.

## 2. Seguridad de Credenciales "Tipo Banco"

> [!TIP]
> **Reto**: Mostrar PINes y Passwords en texto plano en el panel de administración es un riesgo de seguridad.
>
> **Solución**: Implementamos inputs de tipo `password` con un icono de "ojo" (`toggleVisibility`) para visualización temporal. Hasheo seguro mediante `pbkdf2:sha256`.

## 3. Integridad en Navegación (Subdirectorios)

> [!CAUTION]
> **Reto**: Redirecciones de `flask-login` y `url_for` ignorando el prefijo `/rpandemo01/`.
>
> **Solución**: La combinación de `ProxyFix` en Flask y `X-Forwarded-Prefix` en Nginx es mandatoria para navegación bajo subdirectorio.

## 4. Recuperación via WhatsApp

> [!NOTE]
> **Mejora**: El flujo de recuperación mediante enlaces temporales por WhatsApp da autonomía al cliente. El número debe estar sanitizado (sin `+`, `-`, espacios) para la URL `wa.me`.
