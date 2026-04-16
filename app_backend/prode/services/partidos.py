from app_backend.prode.db import get_connection

def listar_partidos():
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
    """)
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
               equipo_local.nombre,
               equipo_visitante.nombre,
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