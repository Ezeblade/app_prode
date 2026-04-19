from datetime import datetime

# Estados válidos para los partidos
ESTADOS_VALIDOS = ['programado', 'en_juego', 'finalizado', 'suspendido']

# Fases válidas del torneo
FASES_VALIDAS = ['grupos', 'octavos', 'cuartos', 'semifinal', 'final', 'tercer_puesto']

def validar_filtros_partidos(tipo_filtro, valor):
    """
    Valida los filtros para el endpoint GET /partidos
    
    Args:
        tipo_filtro (str): Tipo de filtro ('equipo', 'fecha', 'fase', 'estado', 'ciudad')
        valor (str): Valor del filtro a validar
    
    Returns:
        dict: {"valido": bool, "error": str}
    """
    
    if tipo_filtro == "equipo":
        if not valor or len(valor.strip()) == 0:
            return {"valido": False, "error": "El nombre del equipo no puede estar vacío"}
        if len(valor) > 100:
            return {"valido": False, "error": "El nombre del equipo es demasiado largo (máximo 100 caracteres)"}
        return {"valido": True, "error": None}
    
    elif tipo_filtro == "fecha":
        try:
            # Validar formato YYYY-MM-DD
            datetime.strptime(valor, '%Y-%m-%d')
            return {"valido": True, "error": None}
        except ValueError:
            return {"valido": False, "error": "Formato de fecha inválido. Usar YYYY-MM-DD"}
    
    elif tipo_filtro == "fase":
        if valor not in FASES_VALIDAS:
            return {
                "valido": False, 
                "error": f"Fase inválida. Valores permitidos: {', '.join(FASES_VALIDAS)}"
            }
        return {"valido": True, "error": None}
    
    elif tipo_filtro == "estado":
        if valor not in ESTADOS_VALIDOS:
            return {
                "valido": False, 
                "error": f"Estado inválido. Valores permitidos: {', '.join(ESTADOS_VALIDOS)}"
            }
        return {"valido": True, "error": None}
    
    elif tipo_filtro == "ciudad":
        if not valor or len(valor.strip()) == 0:
            return {"valido": False, "error": "La ciudad no puede estar vacía"}
        if len(valor) > 100:
            return {"valido": False, "error": "El nombre de la ciudad es demasiado largo (máximo 100 caracteres)"}
        return {"valido": True, "error": None}
    
    else:
        return {"valido": False, "error": f"Tipo de filtro no soportado: {tipo_filtro}"}
