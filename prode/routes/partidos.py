from flask import Blueprint, jsonify, request
import mysql.connector
from prode.services import partidos as partidos_service
from prode.pagination import parse_pagination_args, build_hateoas_links
from prode.validators import partidos as partidos_validators
# EJEMPLO cuando usen validar o servicios 
#from app_backend.prode.validators.partidos import validar_listado_partidos
#from app_backend.prode.services.partidos import listar_partidos

partidos_bp = Blueprint("partidos", __name__)

# Endpoints Partidos

@partidos_bp.route("/")
def listar_partidos():
    try:
        limit, offset = parse_pagination_args(request.args)
        total = partidos_service.contar_partidos()
        if total == 0:
            return "", 204
        partidos = partidos_service.listar_partidos(limit, offset)
        base_path = request.url_root.rstrip("/") + (request.path or "/")
        links = build_hateoas_links(
            base_path=base_path,
            limit=limit,
            offset=offset,
            total=total,
        )
        return jsonify({"partidos": partidos, "_links": links}), 200
    except ValueError as e:
        return jsonify({
            "errors": [{
                "code": "BAD_REQUEST",
                "message": str (e),
                "level": "error",
            }]
        }), 400
    except Exception as error:
        print(f"error inesperado al crear partido:{str(error)}")
        return jsonify({
            "errors": [{
                "code": "InternalServerError",
                "message": "error al procesar la solicitud",
                "level": "error",
            }]
        }), 500



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
    if not equipo_local or not equipo_visitante or not fecha or not fase or not estadio or not ciudad:
        return jsonify({
            "errors": [{
                "code": "BAD_REQUEST",
                "message": "equipo_local, equipo_visitante, fecha, fase, estadio y ciudad son obligatorios",
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

@partidos_bp.route("/<string:id>", methods=["DELETE"])
def eliminar_partido(id):
    error = partidos_validators.validar_id_entero_positivo(id)
    if error:
        return error
    id = int(id)
    try:
        partido_eliminado = partidos_service.eliminar_partido(id)
    except Exception as error:
        print(f"error inesperado al buscar partido:{str(error)}")
        return jsonify({
            "errors": [{
                "code": "InternalServerError",
                "message": "error al procesar la solicitud",
                "level": "error",
            }]
        }), 500
    if partido_eliminado is False:
            return jsonify({
                "errors": [{
                    "code": "NOT_FOUND",
                    "message": "partido no encontrado",
                    "level": "error",
                }]
        }), 404
    else:
        return "", 204 


@partidos_bp.route("/<string:id>", methods=["GET"])
def obtener_detalle_partido(id):
    error = partidos_validators.validar_id_entero_positivo(id)
    if error:
        return error
    id = int(id)
    try:
        partido = partidos_service.obtener_detalle_partido(id)
        if partido is None:
            return jsonify({
                "errors": [{
                    "code": "NOT_FOUND",
                    "message": "partido no encontrado",
                    "level": "error",
                }]
        }), 404
        return jsonify(partido), 200
    except Exception as error:
        print(f"error inesperado al buscar partido:{str(error)}")
        return jsonify({
            "errors": [{
                "code": "InternalServerError",
                "message": "error al procesar la solicitud",
                "level": "error",
            }]
        }), 500
        
    
   #PUT
@partidos_bp.route("/<string:id>", methods=["PUT"])
def actualizar_partido(id):
    data = request.get_json(silent=True) or {}
    equipo_local = data.get("equipo_local")
    equipo_visitante = data.get("equipo_visitante")
    fecha = data.get("fecha")
    fase = data.get("fase")
    if  not id.isdigit() or int(id) < 1:
        return jsonify({
        "errors": [{
            "code": "BAD_REQUEST",
            "message": "El id debe ser un entero positivo",
            "level": "error",
            }]
        }), 400
    id = int(id)
   
    if  not equipo_local or not equipo_visitante or not fecha or not fase :
        return jsonify({
            "errors": [{
                "code": "BAD_REQUEST",
                "message": "Faltan datos",
                "level": "error",
            }]
    }), 400
    if equipo_local == equipo_visitante:
        return jsonify({
            "errors": [{
                "code": "BAD_REQUEST",
                "message": "Los equipos no pueden ser iguales",
                "level": "error",
                }]
        }), 400 

    try:
        resultado = partidos_service.actualizar_partido(id, equipo_local, equipo_visitante, fecha, fase)
        if not resultado:
            return jsonify({
                "errors": [{
                    "code": "BAD_REQUEST",
                    "message": "No hubieron cambios",
                    "level": "error",
                    }]
            }), 400    
    except Exception as error:
        print(f"error inesperado al buscar partido:{str(error)}")
        return jsonify({
            "errors": [{
                "code": "InternalServerError",
                "message": "error al procesar la solicitud",
                "level": "error",
            }]
        }), 500
    

    return "", 204
#PATCH 
@partidos_bp.route("/<string:id>", methods=["PATCH"])
def actualizar_partido_parcial(id):
    data = request.get_json()  
    error = partidos_validators.validar_id_entero_positivo(id)
    if error:
        return error
    id = int(id)
    if data is None:
        return jsonify({
            "errors": [{
                "code": "BAD_REQUEST",
                "message": "No se enviaron datos",
                "level": "error",
            }]
        }), 400   

    try:
        resultado = partidos_service.actualizar_partido_patch(id, data)
    except Exception as error:
        print(f"error inesperado: {error}")
        return jsonify({
            "errors": [{
                "code": "InternalServerError",
                "message": "error al procesar la solicitud",
                "level": "error",
            }]
        }), 500
    if resultado == "NOT_FOUND":
        return jsonify({
            "errors": [{
                "code": "NOT_FOUND",
                "message": "Partido no encontrado",
                "level": "error",
            }]
        }), 404

    if not resultado:
        return jsonify({
            "errors": [{
                "code": "BAD_REQUEST",
                "message": "No se pudo actualizar",
                "level": "error",
            }]
        }), 400   

    return "", 204


    
   
@partidos_bp.route("/<string:id>/resultado", methods=["PUT"])
def cargar_o_actualizar_resultado(id):
    error = partidos_validators.validar_id_entero_positivo(id)
    if error:
        return error
    id = int(id)
    data = request.get_json(silent=True) or {}
    goles_local = data.get("goles_local")
    goles_visitante = data.get("goles_visitante")

    try:
        gl = int(goles_local)
        gv = int(goles_visitante)

    except (TypeError, ValueError):
        return jsonify({
            "errors": [{
                "code": "BAD_REQUEST",
                "message": "goles_local y goles_visitante deben ser enteros",
                "level": "error",
            }]
        }), 400

    if gl < 0 or gv < 0:
        return jsonify({
            "errors": [{
                "code": "BAD_REQUEST",
                "message": "Los goles no pueden ser negativos",
                "level": "error",
            }]
        }), 400
    try:
        ok = partidos_service.cargar_o_actualizar_resultado(id, gl, gv)
    except Exception as error:
        print(f"error inesperado al actualizar resultado: {error}")
        return jsonify({
            "errors": [{
                "code": "InternalServerError",
                "message": "error al procesar la solicitud",
                "level": "error",
            }]
        }), 500
    if not ok:
        return jsonify({
            "errors": [{
                "code": "NOT_FOUND",
                "message": "Partido no encontrado",
                "level": "error",
            }]
        }), 404
    return "", 204 

