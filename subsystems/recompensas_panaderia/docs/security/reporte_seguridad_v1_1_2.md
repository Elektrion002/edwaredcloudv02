# Reporte Técnico: Blindaje de Seguridad y Accesibilidad Móvil (v1.1.2)

**Proyecto:** EdwaredCloud - Subsistema de Recompensas
**Fecha:** 2026-03-08
**Estado:** PRODUCCIÓN / ESTABLE
**Versión de Seguridad:** 1.1.2

## 1. Contexto y Objetivos

Durante la fase de pruebas del Portal del Cliente, se identificó una advertencia de seguridad emitida por el navegador Google Chrome respecto al uso de credenciales débiles (ej: PIN "5555"). Aunque no representaba una brecha del sistema en sí, indicaba una vulnerabilidad por parte del usuario.

**Objetivos de la intervención:**

- Bloquear el uso de PINs triviales y predecibles.
- Implementar protección contra ataques de fuerza bruta (Brute Force).
- Mantener una experiencia de usuario (UX) fluida, especialmente en dispositivos móviles.

## 2. Implementación Técnica

### 2.1. Módulo de Utilidad: `security.py`

Se creó un componente centralizado `recompensas_app/utils/security.py` para gestionar el **Rate Limiting**.

- **Detección de IP:** El sistema utiliza `request.remote_addr`, el cual está sincronizado con el middleware `ProxyFix` para detectar la IP real del cliente incluso detrás del proxy Nginx del VPS.
- **Whitelist:** Se implementó una lista blanca para `127.0.0.1` y `::1`, evitando bloqueos accidentales a nivel de servidor.
- **Configuración v1.1.2:**
  - Límite de intentos: **10**
  - Tiempo de bloqueo: **3 minutos**

### 2.2. Validación de Credenciales

Se actualizaron los formularios (`PortalLoginForm`, `CustomerForm`, `CustomerUpdateSecretForm`) con validadores personalizados:

- Bloqueo de secuencias comunes: `1234`, `0000`, `2580`, etc.
- Exigencia de longitud mínima y complejidad para contraseñas.

## 3. Resolución de Incidencia v1.1.2 (Accesibilidad Móvil)

Tras la implementación inicial (v1.1.1), se reportó un bloqueo en los campos de login en dispositivos táctiles.

**Causa:** El uso de `pointer-events: none` y el atributo `disabled` en los inputs del formulario causaban fricción con el renderizado móvil, impidiendo la activación del teclado virtual.

**Solución aplicada:**

- Se restauró la interactividad total en los campos `cliente_id` y `secret`.
- El bloqueo de seguridad se trasladó exclusivamente al **botón de envío (Submit)** y a la validación del backend.
- Esto permite al usuario escribir sus credenciales normalmente, pero le impide enviarlas si ha excedido los intentos permitidos.

## 4. Auditoría de Verificación

- **Prueba Staff:** Acceso exitoso mediante PIN seguro. Error visible al intentar PINs débiles.
- **Prueba Portal:** Funcionamiento correcto de la protección anti-fuerza bruta. Al 10to intento, el botón de acceso se deshabilita y muestra un contador de seguridad.
- **Prueba Móvil:** Campos 100% editables y teclado funcional.

## 5. Conclusiones

El sistema de recompensas ahora cuenta con un **Blindaje de Grado Bancario** que protege los puntos de los clientes sin sacrificar la facilidad de uso. Se recomienda al personal del staff guiar a los clientes hacia el uso de PINs no triviales durante su registro inicial.

---

_Generado por Antigravity AI - EdwaredCloud Security Division_
