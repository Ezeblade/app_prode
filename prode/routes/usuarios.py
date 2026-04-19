from flask import Blueprint, jsonify, request
import mysql.connector
from prode.services import usuarios as usuarios_service
from prode.pagination import parse_pagination_args, build_hateoas_links
from prode.validators import usuarios as usuarios_validators
usuarios_bp = Blueprint("usuarios", __name__)

# Endpoints Usuarios

@usuarios_bp.route("/", methods=["GET"])
def listar_usuarios():
    try:
        limit, offset = parse_pagination_args(request.args)
        total = usuarios_service.contar_usuarios()
        if total == 0:
            return "", 204
        usuarios = usuarios_service.listar_usuarios(limit, offset)
        base_path = request.url_root.rstrip("/") + (request.path or "/")
        links = build_hateoas_links(
            base_path=base_path,
            limit=limit,
            offset=offset,
            total=total,
        )
        return jsonify({"usuarios": usuarios, "_links": links}), 200

    except ValueError as e:
        return jsonify({
            "errors": [{
                "code": "BAD_REQUEST",
                "message": str(e),
                "level": "error",
            }]
        }), 400

    except Exception as e:
        print(f"error inesperado al listar usuarios: {e}")
        return jsonify({
            "errors": [{
                "code": "InternalServerError",
                "message": "error al procesar la solicitud",
                "level": "error",
            }]
        }), 500

@usuarios_bp.route("/<string:id>", methods =["GET"])
def obtener_usuario_por_id(id):
    error = usuarios_validators.validar_id_entero_positivo(id)
    if error:
        return error
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
            print(f"error inesperado al crear usuario:{str(error)}")
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
    error = usuarios_validators.validar_id_entero_positivo(id)
    if error:
        return error
    id = int(id)
    data = request.get_json(silent=True) or {}
    nombre = data.get("nombre")
    email = data.get("email")
    if  not email or not nombre:
        return jsonify({
            "errors": [{
                "code": "BAD_REQUEST",
                "message": "Faltan datos",
                "level": "error",
            }]
    }), 400    
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
            print(f"error inesperado al remplzar datos:{str(error)}")
            return jsonify({
                "errors": [{
                    "code": "InternalServerError",
                    "message": "error al procesar la solicitud",
                    "level": "error",
                }]
            }), 500
    return "", 204

@usuarios_bp.route('/<string:id>', methods=['DELETE'])
def eliminar_usuario_por_id(id):
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
        eliminado = usuarios_service.eliminar_usuario_por_id(id)
    except mysql.connector.errors.IntegrityError:
        return jsonify({
            "errors": [{
                "code": "CONFLICT",
                "message": "NO se puede eliminar el usuario porque tiene datos asociados",
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
    if not eliminado:
         return jsonify({
                "errors": [{
                    "code": "NOT_FOUND",
                    "message": "Usuario no encontrado",
                    "level": "error",
                }]
            }), 404
    return "", 204