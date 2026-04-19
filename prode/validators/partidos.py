from flask import jsonify


def validar_id_entero_positivo (id):
    if not id.isdigit() or int(id) < 1:
        return jsonify({
            "errors": [{
                "code": "BAD_REQUEST",
                "message": "El id debe ser un entero positivo",
                "level": "error",
                }]
        }), 400
    
    