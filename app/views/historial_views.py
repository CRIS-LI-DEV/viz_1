# views/historial_views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from app.models import HistorialActuador, HistorialSensor
from app.serializers import HistorialActuadorSerializer, HistorialSensorSerializer
from django.utils.dateparse import parse_datetime
from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware, is_naive
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


class HistorialRangoDatosActuador(APIView):
    """
    Retorna los últimos N registros históricos de un actuador,
    desde una fecha específica hacia atrás, ordenados cronológicamente.
    """
    def get(self, request, id, fecha, n_datos):
        try:
            # Convertir fecha desde string ISO a datetime
            fecha_obj = parse_datetime(fecha)
            if not fecha_obj:
                return Response({'error': 'Formato de fecha inválido.'}, status=status.HTTP_400_BAD_REQUEST)

            # Asegurar zona horaria (timezone-aware)
            if is_naive(fecha_obj):
                fecha_obj = make_aware(fecha_obj)

            n_datos = int(n_datos)

            # Obtener historial desde la fecha hacia atrás
            historial = HistorialActuador.objects.filter(
                actuador_id=id,
                fecha_cambio__lte=fecha_obj
            ).order_by('-fecha_cambio')[:n_datos]

            # Invertir para ordenar de más antiguo a más reciente
            historial = list(historial)[::-1]

            data = [{
                'actuador': h.actuador.nombre,
                'estado': h.estado,
                'fecha': h.fecha_cambio,
                'descripcion': h.descripcion
            } for h in historial]

            return Response({'historial': data}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        



        
class HistorialRangoDatosSensor(APIView):
        def get(self, request, id, fecha, n_datos):
            try:
                fecha_obj = parse_datetime(fecha)
                if not fecha_obj:
                    return Response({'error': 'Formato de fecha inválido.'}, status=status.HTTP_400_BAD_REQUEST)

                # Asegurar que la fecha sea "timezone-aware"
                if is_naive(fecha_obj):
                    fecha_obj = make_aware(fecha_obj)

                n_datos = int(n_datos)

                historial = HistorialActuador.objects.filter(
                    actuador_id=id,
                    fecha_cambio__lte=fecha_obj
                ).order_by('-fecha_cambio')[:n_datos]

                historial = list(historial)[::-1]  # De más antiguo a más reciente

                data = [{
                    'actuador': h.actuador.nombre,
                    'estado': h.estado,
                    'fecha': h.fecha_cambio,
                    'descripcion': h.descripcion
                } for h in historial]

                return Response({'historial': data}, status=status.HTTP_200_OK)

            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
