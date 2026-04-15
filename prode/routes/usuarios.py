from flask import Blueprint, jsonify, request
import mysql.connector
from prode.services import usuarios as usuarios_service
usuarios_bp = Blueprint("usuarios", __name__)

# Endpoints Usuarios

@usuarios_bp.route("/", methods =["GET"])
def listar_usuarios():
    usuarios = usuarios_service.listar_usuarios()
    if not usuarios:
        return "", 204
    return jsonify({"usuarios":usuarios}),200

@usuarios_bp.route("/<string:id>", methods =["GET"])
def obtener_usuario_por_id(id):
    if  not id.isdigit() or int(id) < 1:
        return jsonify({
        "errors": [{
            "code": "BAD_REQUEST",
            "message": "El id debe ser un entero positivo",
            "level": "error",
            }]
        }), 400
    id = int(id)
    try:
        usuario_id = usuarios_service.obtener_usuario_por_id(id)
    except Exception as error:
        print(f"error inesperado al obtener usuario: {error}")
        return jsonify({
            "errors": [{
                "code": "InternalServerError",
                "message": "error al procesar la solicitud",
                "level": "error",
            }]
        }), 500
    if usuario_id is None:
        return jsonify({
            "errors": [{
                "code": "NOT_FOUND",
                "message": "Usuario no encontrado",
                "level": "error",
            }]
        }), 404
    return jsonify(usuario_id), 200

@usuarios_bp.route("/", methods=["POST"])
def crear_usuario():
    data = request.get_json(silent=True) or {}
    nombre = data.get("nombre")
    email = data.get("email")
    if not nombre or not email:
        return jsonify({
            "errors": [{
                "code": "BAD_REQUEST",
                "message": "nombre y email son obligatorios",
                "level": "error",
            }]
        }), 400

    try:
        usuarios_service.crear_usuario(nombre, email)
    except mysql.connector.errors.IntegrityError:
        return jsonify({
            "errors": [{
                "code": "CONFLICT",
                "message": "Email o nombre de usuario ya existente",
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
    return "", 201

@usuarios_bp.route("/<string:id>", methods=["PUT"])
def reemplazar_datos_usuario_por_id(id):
    if  not id.isdigit() or int(id) < 1:
        return jsonify({
        "errors": [{
            "code": "BAD_REQUEST",
            "message": "El id debe ser un entero positivo",
            "level": "error",
            }]
        }), 400
    id = int(id)
    data = request.get_json(silent=True) or {}
    nombre = data.get("nombre")
    email = data.get("email")
    try:
        usuarios_service.reemplazar_datos_usuario_por_id(id, nombre, email)
    except mysql.connector.errors.IntegrityError:
        return jsonify({
            "errors": [{
                "code": "CONFLICT",
                "message": "Email o nombre de usuario ya existente",
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
    return "", 204
