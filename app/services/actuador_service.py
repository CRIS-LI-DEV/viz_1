# services/actuador_service.py
from app.models import HistorialActuador

def get_historial_actuador(actuador_id, numero_registros):
    try:
        historial = HistorialActuador.objects.filter(actuador_id=actuador_id).order_by('-fecha_cambio')[:numero_registros]
        return historial
    except HistorialActuador.DoesNotExist:
        return None
