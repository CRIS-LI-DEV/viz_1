from app.models import HistorialSensor

def get_historial_sensor(sensor_id, numero_registros):
    # Filtra el historial por el ID del sensor y la cantidad de registros que deseas obtener
    historial = HistorialSensor.objects.filter(sensor_id=sensor_id).order_by('-fecha_cambio')[:numero_registros]
    
    if historial.exists():
        return historial
    return None
