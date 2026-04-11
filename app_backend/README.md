# Prode - API Backend

**Introduccion al Desarrollo de Software - TP2**

## Requisitos

- Python 3
- MySQL Server
- pip

## Instalación y ejecución

### 1. Clonar el repositorio

### 2. Entorno virtual y dependencias

Ejemplo creando `venv` dentro de `app_backend`:

```bash
cd app_backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd ..
```

### 3. MySQL - usuario y permisos

En MySQL como administrador, o cambiar credenciales en `app_backend/prode/constants.py`:

```sql
CREATE USER 'alumno'@'localhost' IDENTIFIED BY 'alumno123';
GRANT ALL PRIVILEGES ON *.* TO 'alumno'@'localhost';
FLUSH PRIVILEGES;
```

### 4. Base de datos inicial

Desde la **raiz del repo** (carpeta que contiene `app_backend`):

```bash
cd app_backend/db
python3 init_db.py
cd ../..
```

`init_db.py` abre `init_db.sql` en la misma carpeta (conviene ejecutar estos comandos para que el directorio de trabajo sea el correcto)

### 5. Levantar la API

Con el `venv` activado, desde la **raiz del repo**:

```bash
python3 -m app_backend.app
```
