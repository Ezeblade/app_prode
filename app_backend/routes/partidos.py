from flask import Blueprint, jsonify, request
from app_backend.db import get_connection

partidos_bp = Blueprint("partidos", __name__)

# Endpoints Partidos

@partidos_bp.route("/")
def get_partidos():
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
    return jsonify(partidos)
