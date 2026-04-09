from flask import Blueprint, jsonify, request
from app_backend.db import get_connection

prediccion_bp = Blueprint("prediccion", __name__)

# Endpoints Prediccion