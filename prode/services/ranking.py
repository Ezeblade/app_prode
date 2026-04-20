from prode.db import get_connection


def contar_usuarios_ranking() -> int:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM usuario")
    total = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return total


def listar_ranking(limit: int, offset: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT u.id AS id_usuario, COALESCE(t.puntos, 0) AS puntos
        FROM usuario u
        LEFT JOIN (
            SELECT
                p.id_usuario,
                SUM(
                    CASE
                        WHEN p.goles_local = pt.goles_local
                             AND p.goles_visitante = pt.goles_visitante THEN 3
                        WHEN (
                            (pt.goles_local > pt.goles_visitante
                             AND p.goles_local > p.goles_visitante)
                            OR (pt.goles_local < pt.goles_visitante
                                AND p.goles_local < p.goles_visitante)
                            OR (pt.goles_local = pt.goles_visitante
                                AND p.goles_local = p.goles_visitante)
                        ) THEN 1
                        ELSE 0
                    END
                ) AS puntos
            FROM prediccion p
            INNER JOIN partido pt ON p.id_partido = pt.id
            WHERE pt.goles_local IS NOT NULL
              AND pt.goles_visitante IS NOT NULL
            GROUP BY p.id_usuario
        ) t ON u.id = t.id_usuario
        ORDER BY puntos DESC, id_usuario ASC
        LIMIT %s OFFSET %s
        """,
        (limit, offset),
    )
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    for row in rows:
        row["puntos"] = int(row["puntos"])
    return rows