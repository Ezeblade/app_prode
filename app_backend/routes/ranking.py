from flask import Blueprint, jsonify, request
from app_backend.db import get_connection

ranking_bp = Blueprint("ranking", __name__)

# Endpoints Ranking