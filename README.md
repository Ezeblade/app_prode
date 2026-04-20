<h1 align="center">Prode API Backend</h1>

<p align="center">
  Trabajo practico de Introduccion al Desarrollo de Software
</p>

---

## Documentacion visual (Figma)

¿Preferís una versión más **humana** de la estructura del proyecto y cómo se conectan las partes? Podés recorrer un mapa visual en Figma:

**[Abrir documentación en Figma](https://www.figma.com/board/GXqhcdx0lXW3IxPF8AVash/Proyecto-PRODE-TP2?node-id=0-1&t=AWZF5SoyLj2FuLN4-1)**

Ahí está resumida la organización del código de forma más gráfica que leyendo solo carpetas y archivos.

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
source venv/bin/activate   # Windows: venv\Scripts\activate
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
python3 -m app
```

Base URL:

- `http://127.0.0.1:5000`

---

## Supuestos e hipotesis

- La API usa MySQL local (`localhost`) y la base `prode`.
- Rutas principales: `partidos`, `usuarios`, `predicciones` (montado con prefijo `/partidos` para el POST de prediccion) y `ranking`.
- **Usuarios:** para crear un usuario son obligatorios **`nombre`** y **`email`** (contrato OpenAPI). Los valores suelen ser únicos en base; si se repiten, la API puede responder **409 Conflict**.
- **Usuarios:** el **listado** y el **detalle** pueden no devolver exactamente los mismos campos (por ejemplo resumen con `id` / `nombre_usuario` en el listado y `nombre` / `email` en el detalle), según la implementación actual.
- **Usuarios:** el **PUT** `/usuarios/{id}` puede comportarse como *upsert* (reemplazar si existe; crear fila con ese `id` si no existe), según lo documentado en esta guía.
- En partidos:
  - `POST /partidos/` usa IDs de equipos.
  - `PUT /partidos/{id}` y `PATCH /partidos/{id}` usan nombres de equipos (`equipo_local`, `equipo_visitante`).
- `fase_torneo` debe respetar estos valores: `grupos`, `dieciseisavos`, `octavos`, `cuartos`, `semis`, `final`.
- **Predicciones:** solo se permiten si el partido existe y aun no tiene resultado cargado (`goles_local` y `goles_visitante` en `NULL`). Una prediccion por usuario y partido.
- **Ranking:** los puntos se calculan dinamicamente comparando predicciones con resultados ya cargados (no se usa la tabla `ranking` para el GET). Criterio: marcador exacto 3 puntos; mismo desenlace (ganador o empate) con marcador distinto 1 punto; resto 0.

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
| ![PUT](https://img.shields.io/badge/PUT-f0883e?style=flat-square) | `/partidos/{id}/resultado` | Cargar o actualizar resultado |
| ![POST](https://img.shields.io/badge/POST-2ea043?style=flat-square) | `/partidos/{id}/prediccion` | Registrar prediccion |

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
- ![400](https://img.shields.io/badge/400-Bad_Request-c93c37?style=flat-square) Mal ingreso de datos
- ![404](https://img.shields.io/badge/404-Not_Found-c93c37?style=flat-square)  No existe el partido con ese ID
- ![500](https://img.shields.io/badge/500-Internal_Server_Error-c93c37?style=flat-square)

### 4) Eliminar partido

- URL: `http://127.0.0.1:5000/partidos/{id}`

Respuestas:

- ![204](https://img.shields.io/badge/204-No_Content-2ea043?style=flat-square)
- ![400](https://img.shields.io/badge/400-Bad_Request-c93c37?style=flat-square) No existe partido con ese ID
- ![404](https://img.shields.io/badge/404-Not_Found-c93c37?style=flat-square)  El id es negativo o 0
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
- ![400](https://img.shields.io/badge/400-Bad_Request-c93c37?style=flat-square) El ID no puede ser negativo o 0
- ![404](https://img.shields.io/badge/404-Not_Found-c93c37?style=flat-square)  No existe partido con ese ID
- ![500](https://img.shields.io/badge/500-Internal_Server_Error-c93c37?style=flat-square)

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
- ![400](https://img.shields.io/badge/400-Bad_Request-c93c37?style=flat-square) El ID no puede ser negativo o 0 | No pueden faltar campos
- ![404](https://img.shields.io/badge/404-Not_Found-c93c37?style=flat-square)  No existe partido con ese ID
- ![500](https://img.shields.io/badge/500-Internal_Server_Error-c93c37?style=flat-square)

### 7) Cargar o actualizar resultado

- URL: `http://127.0.0.1:5000/partidos/{id}/resultado`

Body:

```json
{
  "goles_local": 2,
  "goles_visitante": 1
}
```

Respuestas:

- ![204](https://img.shields.io/badge/204-No_Content-2ea043?style=flat-square)
- ![400](https://img.shields.io/badge/400-Bad_Request-c93c37?style=flat-square) El id no puede ser negativo o 0 | Los goles deben ser positivos 
- ![404](https://img.shields.io/badge/404-Not_Found-c93c37?style=flat-square) No existe partido con ese ID
- ![500](https://img.shields.io/badge/500-Internal_Server_Error-c93c37?style=flat-square)

---

## Usuarios

### Endpoints disponibles

| Metodo | URL | Descripcion |
|---|---|---|
| ![GET](https://img.shields.io/badge/GET-1f6feb?style=flat-square) | `/usuarios/` | Listar usuarios |
| ![GET](https://img.shields.io/badge/GET-1f6feb?style=flat-square) | `/usuarios/{id}` | Obtener usuario |
| ![POST](https://img.shields.io/badge/POST-2ea043?style=flat-square) | `/usuarios/` | Crear usuario |
| ![PUT](https://img.shields.io/badge/PUT-f0883e?style=flat-square) | `/usuarios/{id}` | Reemplazar usuario |
| ![DELETE](https://img.shields.io/badge/DELETE-c93c37?style=flat-square) | `/usuarios/{id}` | Eliminar usuario |

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
- ![400](https://img.shields.io/badge/400-Bad_Request-c93c37?style=flat-square) El ID no puede ser negativo o 0
- ![404](https://img.shields.io/badge/404-Not_Found-c93c37?style=flat-square)   No existe usuario con ese ID
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
- ![400](https://img.shields.io/badge/400-Bad_Request-c93c37?style=flat-square) No puede haber campos vacios
- ![409](https://img.shields.io/badge/409-Conflict-c93c37?style=flat-square) Si email y/o nombre ya existente
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
- ![400](https://img.shields.io/badge/400-Bad_Request-c93c37?style=flat-square) El ID no puede ser negativo o 0 | No puede haber campos vacios
- ![409](https://img.shields.io/badge/409-Conflict-c93c37?style=flat-square) Si email y/o nombre ya existente
- ![500](https://img.shields.io/badge/500-Internal_Server_Error-c93c37?style=flat-square)

### 5) Eliminar usuario por ID

- URL: `http://127.0.0.1:5000/usuarios/{id}`

Body:

```json
{

}
```

Respuestas:

- ![204](https://img.shields.io/badge/204-No_Content-2ea043?style=flat-square)
- ![400](https://img.shields.io/badge/400-Bad_Request-c93c37?style=flat-square) El ID no puede ser negativo o 0 
- ![404](https://img.shields.io/badge/404-Not_Found-c93c37?style=flat-square)   No existe usuario con ese ID
- ![409](https://img.shields.io/badge/409-Conflict-c93c37?style=flat-square) Si tiene datos asociados con Ranking/Prediccion
- ![500](https://img.shields.io/badge/500-Internal_Server_Error-c93c37?style=flat-square)


---

## Predicciones y ranking

### Prediccion

| Metodo | URL | Descripcion |
|---|---|---|
| ![POST](https://img.shields.io/badge/POST-2ea043?style=flat-square) | `/partidos/{id}/prediccion` | Registrar prediccion para un partido |

- URL ejemplo: `http://127.0.0.1:5000/partidos/1/prediccion`

Body (segun contrato OpenAPI):

```json
{
  "id_usuario": 2,
  "local": 2,
  "visitante": 1
}
```

(`local` y `visitante` son los goles predichos para local y visitante.)

Respuestas:

- ![201](https://img.shields.io/badge/201-Created-2ea043?style=flat-square) cuerpo vacio o minimo.
- ![400](https://img.shields.io/badge/400-Bad_Request-c93c37?style=flat-square) datos invalidos, goles negativos, partido con resultado ya cargado, etc.
- ![404](https://img.shields.io/badge/404-Not_Found-c93c37?style=flat-square) partido o usuario inexistente.
- ![409](https://img.shields.io/badge/409-Conflict-c93c37?style=flat-square) prediccion duplicada (mismo usuario y mismo partido).
- ![500](https://img.shields.io/badge/500-Internal_Server_Error-c93c37?style=flat-square)

**Nota:** En `app.py`, el blueprint de predicciones debe estar registrado con `url_prefix="/partidos"` (forma B) para que la URL sea exactamente `/partidos/{id}/prediccion`. Si en tu proyecto la ruta esta colgada de `partidos_bp` en `partidos.py` o se carga con un `import` lateral, la URL visible debe coincidir con esta.

### Ranking

| Metodo | URL | Descripcion |
|---|---|---|
| ![GET](https://img.shields.io/badge/GET-1f6feb?style=flat-square) | `/ranking` | Ranking de usuarios por puntos |

Parametros de paginacion (query):

- `_limit` (por defecto 10 en el proyecto)
- `_offset`

Ejemplo:

`http://127.0.0.1:5000/ranking?_limit=10&_offset=0`

Respuestas:

- ![200](https://img.shields.io/badge/200-OK-2ea043?style=flat-square)
- ![204](https://img.shields.io/badge/204-No_Content-9a6700?style=flat-square) si no hay usuarios en la base.
- ![400](https://img.shields.io/badge/400-Bad_Request-c93c37?style=flat-square) paginacion invalida.
- ![500](https://img.shields.io/badge/500-Internal_Server_Error-c93c37?style=flat-square)

Ejemplo de cuerpo exitoso:

```json
{
  "ranking": [
    { "id_usuario": 2, "puntos": 4 },
    { "id_usuario": 1, "puntos": 0 }
  ],
  "_links": {
    "_first": { "href": "..." },
    "_last": { "href": "..." }
  }
}
```

Incluye enlaces HATEOAS (`_first`, `_prev`, `_next`, `_last` cuando aplica), igual que listados paginados.

---

## Estructura principal

- `app.py`: crea la aplicacion Flask y registra blueprints.
- `db/init_db.sql`: esquema de base y datos iniciales.
- `prode/routes/`: handlers HTTP.
- `prode/services/`: acceso a datos y logica.
- `docs/swagger.yaml`: contrato OpenAPI de referencia.
