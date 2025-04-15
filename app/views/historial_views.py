# views/historial_views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from app.models import HistorialActuador, HistorialSensor
from app.serializers import HistorialActuadorSerializer, HistorialSensorSerializer

class HistorialActuadorAPIView(APIView):
    def get(self, request, id, numero_registros):
        historial = HistorialActuador.objects.filter(actuador_id=id).order_by('-fecha_cambio')[:numero_registros]
        if not historial:
            return Response({"error": "No se encontraron registros."}, status=status.HTTP_404_NOT_FOUND)
        serializer = HistorialActuadorSerializer(historial, many=True)
        return Response(serializer.data)


class HistorialSensorAPIView(APIView):
    def get(self, request, id, numero_registros):
        historial = HistorialSensor.objects.filter(sensor_id=id).order_by('-fecha_cambio')[:numero_registros]
            
        if not historial:
            return Response({"error": "No se encontraron registros."}, status=status.HTTP_404_NOT_FOUND)
        serializer = HistorialSensorSerializer(historial, many=True)
        return Response(serializer.data)