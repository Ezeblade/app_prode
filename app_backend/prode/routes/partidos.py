from flask import Blueprint, jsonify, request
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

