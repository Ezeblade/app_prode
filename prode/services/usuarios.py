from prode.db import get_connection

def listar_usuarios():

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT id, nombre_usuario 
        FROM usuario 
        ORDER BY id
    """)

    usuarios = cursor.fetchall()
    cursor.close()
    conn.close()
    return usuarios

def obtener_usuario_por_id(usuario_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT id,nombre_usuario AS nombre, email
        FROM usuario
        WHERE id = %s
        """, (usuario_id,),
    )

    usuario_id = cursor.fetchone()
    cursor.close()
    conn.close()
    return usuario_id

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

