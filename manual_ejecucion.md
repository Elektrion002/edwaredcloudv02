# Guía de Ejecución Manual - EdwaredCloud v2

Esta guía detalla los pasos para levantar la aplicación de forma manual en un entorno Windows.

## 1. Requisitos Previos

Asegúrese de estar en el directorio raíz del proyecto:
`d:\VPS_Edwared_v02`

## 2. Activar el Entorno Virtual (venv)

El entorno virtual aísla las dependencias del proyecto. Para activarlo, ejecute el siguiente comando en su terminal (PowerShell o CMD):

### En PowerShell:

```powershell
.\venv\Scripts\activate
```

### En CMD (Símbolo del sistema):

```cmd
venv\Scripts\activate
```

_Sabrá que está activo porque aparecerá `(venv)` al principio de su línea de comandos._

## 3. Instalar Dependencias (Solo la primera vez)

Si es la primera vez que inicia el proyecto o ha agregado nuevas librerías:

```bash
pip install -r requirements.txt
```

## 4. Iniciar la Aplicación

Una vez activado el entorno, ejecute el archivo principal:

```bash
python run.py
```

La aplicación estará disponible en: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## Solución de Problemas Comunes

### Error de Ejecución de Scripts en PowerShell

Si PowerShell bloquea la activación del venv, ejecute este comando como administrador una sola vez:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### El comando 'python' no se reconoce

Asegúrese de tener Python instalado y agregado al PATH, o intente usar `py run.py`.
