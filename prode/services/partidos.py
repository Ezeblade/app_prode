from prode.db import get_connection

def contar_partidos():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM partido")
    total = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return total

def listar_partidos(limit: int, offset: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT p.id,
               el.nombre AS equipo_local,
               ev.nombre AS equipo_visitante,
               p.fecha_partido AS fecha,
               p.fase_torneo AS fase
        FROM partido p
        JOIN equipo el ON p.id_equipo_local = el.id
        JOIN equipo ev ON p.id_equipo_visitante = ev.id
        ORDER BY p.id
        LIMIT %s OFFSET %s
        """,
        (limit, offset),
        )
    partidos = cursor.fetchall()
    cursor.close()
    conn.close()
    return partidos


def crear_partido(equipo_local: int, equipo_visitante: int, estadio: str, ciudad: str, fecha: str, fase: str, goles_local: int, goles_visitante: int) -> int:
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        INSERT INTO partido (id_equipo_local, id_equipo_visitante, estadio, ciudad, fecha_partido, fase_torneo, goles_local, goles_visitante)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (equipo_local, equipo_visitante, estadio, ciudad, fecha, fase, goles_local, goles_visitante),
    )
    conn.commit()
    nuevo_partido = cursor.lastrowid
    cursor.close()
    conn.close()
    return nuevo_partido

def obtener_detalle_partido(id_partido: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT partido.id,
               equipo_local.nombre AS equipo_local,
               equipo_visitante.nombre AS equipo_visitante,
               partido.estadio,
               partido.ciudad,
               partido.fecha_partido,
               partido.fase_torneo,
               partido.goles_local,
               partido.goles_visitante
        FROM partido 
        JOIN equipo equipo_local ON partido.id_equipo_local = equipo_local.id
        JOIN equipo equipo_visitante ON partido.id_equipo_visitante = equipo_visitante.id
        WHERE partido.id = %s
    """, (id_partido,)
    )
    partido = cursor.fetchone()
    cursor.close()
    conn.close()
    return partido

def eliminar_partido(id_partido:int):
    conn= get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("DELETE FROM prediccion WHERE id_partido = %s", (id_partido,))
    cursor.execute("DELETE FROM partido WHERE id = %s", (id_partido,))
    conn.commit()
    filas_eliminadas = cursor.rowcount
    cursor.close()
    conn.close()
    return filas_eliminadas > 0 

#Obtener ID de equipo
def obtener_id_equipo(nombre):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM equipo WHERE nombre = %s", (nombre,))
    resultado = cursor.fetchone()
    cursor.close()
    conn.close()
    return resultado[0] if resultado else None


def actualizar_partido(id, equipo_local, equipo_visitante, fecha, fase):
    id_local = obtener_id_equipo(equipo_local)
    id_visitante = obtener_id_equipo(equipo_visitante)

    if not id_local or not id_visitante:
        return False

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE partido
        SET id_equipo_local = %s,
            id_equipo_visitante = %s,
            fecha_partido = %s,
            fase_torneo = %s
        WHERE id = %s
        """,
        (id_local, id_visitante, fecha, fase, id)
    )
    conn.commit()

    filas = cursor.rowcount
    cursor.close()
    conn.close()
    return filas > 0
#PATCH 
def actualizar_partido_patch(id,data):
    partes = []
    valores = []

    # Validaciones de equipos
    if "equipo_local" in data:
        id_local = obtener_id_equipo(data["equipo_local"])
        if id_local is None:
            return False
        partes.append("id_equipo_local = %s")
        valores.append(id_local)

    if "equipo_visitante" in data:
        id_visitante = obtener_id_equipo(data["equipo_visitante"])
        if id_visitante is None:
            return False
        partes.append("id_equipo_visitante = %s")
        valores.append(id_visitante)

    if "fecha" in data:
        partes.append("fecha_partido = %s")
        valores.append(data["fecha"])

    if "fase" in data:
        partes.append("fase_torneo = %s")
        valores.append(data["fase"])

    # Evita UPDATE vacío
    if not partes:
        return False  

    conn = get_connection()
    cursor = conn.cursor() 

    # Verificamos si existe el partido (para 404)
    cursor.execute("SELECT id FROM partido WHERE id = %s", (id,))
    if cursor.fetchone() is None:
        cursor.close()
        conn.close()
        return "NOT_FOUND" 

    # UPDATE
    query = "UPDATE partido SET " + ", ".join(partes) + " WHERE id = %s"
    valores.append(id)

    cursor.execute(query, valores)
    conn.commit()

    cursor.close()
    conn.close()

    return True  


def cargar_o_actualizar_resultado(id_partido, goles_local, goles_visitante):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM partido WHERE id = %s", (id_partido,))
    existe = cursor.fetchone() is not None
    if not existe:
        cursor.close()
        conn.close()
        return False
    cursor.execute(
        """
        UPDATE partido 
        SET goles_local = %s, goles_visitante = %s
        WHERE id = %s
        """, 
        (goles_local,goles_visitante,id_partido),
    )
    conn.commit()
    cursor.close()
    conn.close()
    return True