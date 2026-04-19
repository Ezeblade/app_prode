from flask import Blueprint, jsonify, request

from prode.pagination import parse_pagination_args, build_hateoas_links
from prode.services import ranking as ranking_service

ranking_bp = Blueprint("ranking", __name__)


@ranking_bp.route("/", methods=["GET"])
def obtener_ranking():
    try:
        limit, offset = parse_pagination_args(request.args)
        total = ranking_service.contar_usuarios_ranking()
        if total == 0:
            return "", 204
        filas = ranking_service.listar_ranking(limit, offset)
        base_path = request.url_root.rstrip("/") + (request.path or "/")
        links = build_hateoas_links(
            base_path=base_path,
            limit=limit,
            offset=offset,
            total=total,
        )
        return jsonify({"ranking": filas, "_links": links}), 200
    except ValueError as e:
        return jsonify({
            "errors": [{
                "code": "BAD_REQUEST",
                "message": str(e),
                "level": "error",
            }]
        }), 400
    except Exception as e:
        print(f"error inesperado al obtener ranking: {e}")
        return jsonify({
            "errors": [{
                "code": "InternalServerError",
                "message": "error al procesar la solicitud",
                "level": "error",
            }]
        }), 500