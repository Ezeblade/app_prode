from app_backend.prode.db import get_connection

def listar_usuarios():

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT id, nombre_usuario FROM usuario ORDER BY id
    """)

    usuarios = cursor.fetchall()
    cursor.close()
    conn.close()
    return usuarios

def crear_usuario(nombre: str, email: str) -> int:

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO usuario (nombre_usuario, email)
        VALUES (%s, %s)
        """,
        (nombre, email),
    )
    conn.commit()
    nuevo_usuario = cur.lastrowid
    cur.close()
    conn.close()
    return nuevo_usuario