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


def crear_partido(equipo_local: int, id_equipo_local: int, estadio: str, ciudad: str, fecha: str, fase: str, goles_local: int, goles_visitante: int) -> int:
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
    cur.close()
    conn.close()
    return nuevo_partido
