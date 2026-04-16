from flask import Blueprint, jsonify, request
import mysql.connector
from app_backend.prode.db import get_connection
from app_backend.prode.services import partidos as partidos_service
# EJEMPLO cuando usen validar o servicios 
#from app_backend.prode.validators.partidos import validar_listado_partidos
#from app_backend.prode.services.partidos import listar_partidos

partidos_bp = Blueprint("partidos", __name__)

# Endpoints Partidos

@partidos_bp.route("/")
def listar_partidos():
    partidos = partidos_service.listar_partidos()
    if not partidos:
        return "", 204
    return jsonify(partidos)

@partidos_bp.route("/", methods=["POST"])
def crear_partido():
    data = request.get_json(silent=True) or {}
    equipo_local = data.get("id_equipo_local")
    equipo_visitante = data.get("id_equipo_visitante")
    estadio = data.get("estadio")
    ciudad = data.get("ciudad")
    fecha = data.get("fecha_partido")
    fase = data.get("fase_torneo")
    goles_local = data.get("goles_local")
    goles_visitante = data.get("goles_visitante")
    if not equipo_local or not equipo_visitante or not fecha or not fase:
        return jsonify({
            "errors": [{
                "code": "BAD_REQUEST",
                "message": "equipo_local, equipo_visitante, fecha y fase son obligatorios",
                "level": "error",
            }]
        }), 400
    
    try:
        partidos_service.crear_partido(equipo_local, equipo_visitante, estadio, ciudad, fecha, fase, goles_local, goles_visitante)
        return jsonify({
            "code": "CREATED",
            "message": "partido creado exitosamente",
            "level": "info",
        }), 201
    except mysql.connector.errors.IntegrityError:
        return jsonify({
            "errors": [{
                "code": "CONFLICT",
                "message": "datos ya existentes",
                "level": "error",
            }]
        }), 409
    except Exception as error:
        print(f"error inesperado al crear partido:{str(error)}")
        return jsonify({
            "errors": [{
                "code": "InternalServerError",
                "message": "error al procesar la solicitud",
                "level": "error",
            }]
        }), 500