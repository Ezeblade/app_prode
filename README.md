<h1 align="center">Prode API Backend</h1>

<p align="center">
  Trabajo practico de Introduccion al Desarrollo de Software
</p>

---

## Indice

- [Requisitos](#requisitos)
- [Instalacion y ejecucion](#instalacion-y-ejecucion)
- [Supuestos e hipotesis](#supuestos-e-hipotesis)
- [Errores comunes](#errores-comunes)
- [Ejemplos de uso](#ejemplos-de-uso)
  - [Partidos](#partidos)
  - [Usuarios](#usuarios)
  - [Predicciones y ranking](#predicciones-y-ranking)
- [Estructura principal](#estructura-principal)

---

## Requisitos

- Python 3
- MySQL Server
- pip

---

## Instalacion y ejecucion

### 1) Clonar el repositorio

```bash
git clone <url-del-repo>
cd app_prode
```

### 2) Crear entorno virtual e instalar dependencias

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3) Configurar usuario y permisos en MySQL

Si vas a usar los valores por defecto del proyecto (archivo `prode/constants.py`), crea el usuario:

```sql
CREATE USER 'alumno'@'localhost' IDENTIFIED BY 'alumno123';
GRANT ALL PRIVILEGES ON *.* TO 'alumno'@'localhost';
FLUSH PRIVILEGES;
```

Si usas otro usuario o password, actualiza `DB_HOST`, `DB_USER`, `DB_PASSWORD` y `DB_NAME` en `prode/constants.py`.

### 4) Crear base de datos y datos iniciales

Desde la carpeta `app_prode`:

```bash
python3 -m db.init_db
```

Esto crea la base `prode`, tablas y datos de ejemplo definidos en `db/init_db.sql`.

### 5) Levantar la API

Con el entorno virtual activado y desde `app_prode`:

```bash
python3 -m app.py
```

Base URL:

- `http://127.0.0.1:5000`

---

## Supuestos e hipotesis

- La API usa MySQL local (`localhost`) y la base `prode`.
- Las rutas activas hoy son `partidos` y `usuarios`.
- Los blueprints `predicciones` y `ranking` estan registrados, pero sin endpoints expuestos.
- En partidos:
  - `POST /partidos/` usa IDs de equipos.
  - `PUT /partidos/{id}` y `PATCH /partidos/{id}` usan nombres de equipos (`equipo_local`, `equipo_visitante`).
- `fase_torneo` debe respetar estos valores: `grupos`, `dieciseisavos`, `octavos`, `cuartos`, `semis`, `final`.

---

## Errores comunes

Si recibes `500 InternalServerError`, revisar:

- Entorno virtual no activado.
- Dependencias sin instalar.
- MySQL apagado o credenciales incorrectas.
- Base de datos no inicializada.

---

## Ejemplos de uso

## Partidos

### Endpoints disponibles

| Metodo | URL | Descripcion |
|---|---|---|
| ![GET](https://img.shields.io/badge/GET-1f6feb?style=flat-square) | `/partidos/` | Listar partidos |
| ![POST](https://img.shields.io/badge/POST-2ea043?style=flat-square) | `/partidos/` | Crear partido |
| ![GET](https://img.shields.io/badge/GET-1f6feb?style=flat-square) | `/partidos/{id}` | Obtener detalle |
| ![DELETE](https://img.shields.io/badge/DELETE-c93c37?style=flat-square) | `/partidos/{id}` | Eliminar partido |
| ![PUT](https://img.shields.io/badge/PUT-f0883e?style=flat-square) | `/partidos/{id}` | Reemplazo total |
| ![PATCH](https://img.shields.io/badge/PATCH-8250df?style=flat-square) | `/partidos/{id}` | Actualizacion parcial |

### 1) Listar partidos

- URL: `http://127.0.0.1:5000/partidos/`

Respuesta exitosa:

- ![200](https://img.shields.io/badge/200-OK-2ea043?style=flat-square)
- ![204](https://img.shields.io/badge/204-No_Content-9a6700?style=flat-square)

Ejemplo:

```json
[
  {
    "id": 1,
    "equipo_local": "ARGENTINA",
    "equipo_visitante": "BRASIL",
    "fecha": "Wed, 12 Aug 2026 07:30:00 GMT",
    "fase": "final"
  }
]
```

### 2) Crear partido

- URL: `http://127.0.0.1:5000/partidos/`

Body:

```json
{
  "id_equipo_local": 2,
  "id_equipo_visitante": 3,
  "estadio": "London Stadium",
  "ciudad": "Londres",
  "fecha_partido": "2026-08-12 07:30:00",
  "fase_torneo": "final",
  "goles_local": 2,
  "goles_visitante": 1
}
```

Respuestas:

- ![201](https://img.shields.io/badge/201-Created-2ea043?style=flat-square)

```json
{
  "code": "CREATED",
  "message": "partido creado exitosamente",
  "level": "info"
}
```

- ![400](https://img.shields.io/badge/400-Bad_Request-c93c37?style=flat-square) si faltan obligatorios.
- ![409](https://img.shields.io/badge/409-Conflict-c93c37?style=flat-square) si hay conflicto de integridad.
- ![500](https://img.shields.io/badge/500-Internal_Server_Error-c93c37?style=flat-square) en errores no controlados.

### 3) Obtener detalle de partido por ID

- URL: `http://127.0.0.1:5000/partidos/{id}`

Respuestas:

- ![200](https://img.shields.io/badge/200-OK-2ea043?style=flat-square)
- ![400](https://img.shields.io/badge/400-Bad_Request-c93c37?style=flat-square)
- ![404](https://img.shields.io/badge/404-Not_Found-c93c37?style=flat-square)
- ![500](https://img.shields.io/badge/500-Internal_Server_Error-c93c37?style=flat-square)

### 4) Eliminar partido

- URL: `http://127.0.0.1:5000/partidos/{id}`

Respuestas:

- ![204](https://img.shields.io/badge/204-No_Content-2ea043?style=flat-square)
- ![404](https://img.shields.io/badge/404-Not_Found-c93c37?style=flat-square)
- ![500](https://img.shields.io/badge/500-Internal_Server_Error-c93c37?style=flat-square)

### 5) Reemplazo total de partido

- URL: `http://127.0.0.1:5000/partidos/{id}`

Body:

```json
{
  "equipo_local": "ARGENTINA",
  "equipo_visitante": "BRASIL",
  "fecha": "2026-12-18 20:00:00",
  "fase": "final"
}
```

Respuestas:

- ![204](https://img.shields.io/badge/204-No_Content-2ea043?style=flat-square)
- ![400](https://img.shields.io/badge/400-Bad_Request-c93c37?style=flat-square)

### 6) Actualizacion parcial de partido

- URL: `http://127.0.0.1:5000/partidos/{id}`

Body:

```json
{
  "fase": "semis",
  "equipo_visitante": "FRANCIA"
}
```

Respuestas:

- ![204](https://img.shields.io/badge/204-No_Content-2ea043?style=flat-square)
- ![400](https://img.shields.io/badge/400-Bad_Request-c93c37?style=flat-square)
- ![404](https://img.shields.io/badge/404-Not_Found-c93c37?style=flat-square)

---

## Usuarios

### Endpoints disponibles

| Metodo | URL | Descripcion |
|---|---|---|
| ![GET](https://img.shields.io/badge/GET-1f6feb?style=flat-square) | `/usuarios/` | Listar usuarios |
| ![GET](https://img.shields.io/badge/GET-1f6feb?style=flat-square) | `/usuarios/{id}` | Obtener usuario |
| ![POST](https://img.shields.io/badge/POST-2ea043?style=flat-square) | `/usuarios/` | Crear usuario |
| ![PUT](https://img.shields.io/badge/PUT-f0883e?style=flat-square) | `/usuarios/{id}` | Reemplazar usuario |

### 1) Listar usuarios

- URL: `http://127.0.0.1:5000/usuarios/`

Respuestas:

- ![200](https://img.shields.io/badge/200-OK-2ea043?style=flat-square)
- ![204](https://img.shields.io/badge/204-No_Content-9a6700?style=flat-square)

Ejemplo:

```json
{
  "usuarios": [
    {
      "id": 1,
      "nombre_usuario": "azul10"
    }
  ]
}
```

### 2) Obtener usuario por ID

- URL: `http://127.0.0.1:5000/usuarios/{id}`

Respuestas:

- ![200](https://img.shields.io/badge/200-OK-2ea043?style=flat-square)
- ![400](https://img.shields.io/badge/400-Bad_Request-c93c37?style=flat-square)
- ![404](https://img.shields.io/badge/404-Not_Found-c93c37?style=flat-square)
- ![500](https://img.shields.io/badge/500-Internal_Server_Error-c93c37?style=flat-square)

Ejemplo:

```json
{
  "id": 1,
  "nombre": "azul10",
  "email": "azulita@gmail.com"
}
```

### 3) Crear usuario

- URL: `http://127.0.0.1:5000/usuarios/`

Body:

```json
{
  "nombre": "nuevo_usuario",
  "email": "nuevo@mail.com"
}
```

Respuestas:

- ![201](https://img.shields.io/badge/201-Created-2ea043?style=flat-square)
- ![400](https://img.shields.io/badge/400-Bad_Request-c93c37?style=flat-square)
- ![409](https://img.shields.io/badge/409-Conflict-c93c37?style=flat-square)
- ![500](https://img.shields.io/badge/500-Internal_Server_Error-c93c37?style=flat-square)

### 4) Reemplazar usuario por ID

- URL: `http://127.0.0.1:5000/usuarios/{id}`

Body:

```json
{
  "nombre": "usuario_editado",
  "email": "editado@mail.com"
}
```

Respuestas:

- ![204](https://img.shields.io/badge/204-No_Content-2ea043?style=flat-square)
- ![400](https://img.shields.io/badge/400-Bad_Request-c93c37?style=flat-square)
- ![409](https://img.shields.io/badge/409-Conflict-c93c37?style=flat-square)
- ![500](https://img.shields.io/badge/500-Internal_Server_Error-c93c37?style=flat-square)

Nota: este endpoint funciona como upsert. Si el ID no existe, crea un usuario con ese ID.

---

## Predicciones y ranking

Actualmente los blueprints `predicciones` y `ranking` estan registrados en la app, pero todavia no exponen endpoints HTTP.

---

## Estructura principal

- `app.py`: crea la aplicacion Flask y registra blueprints.
- `db/init_db.sql`: esquema de base y datos iniciales.
- `prode/routes/`: handlers HTTP.
- `prode/services/`: acceso a datos y logica.
