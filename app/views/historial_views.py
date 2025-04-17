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
        # Validar fecha
        fecha_obj = parse_datetime(fecha)
        if not fecha_obj:
            return Response({'error': 'Formato de fecha inválido.'}, status=status.HTTP_400_BAD_REQUEST)

        # Asegurar que sea timezone-aware
        if is_naive(fecha_obj):
            fecha_obj = make_aware(fecha_obj)

        # Validar número de datos
        try:
            n_datos = int(n_datos)
        except ValueError:
            return Response({'error': 'n_datos debe ser un número entero.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Obtener los últimos N registros antes de la fecha, optimizando acceso
            historial = list(
                HistorialActuador.objects.filter(
                    actuador_id=id,
                    fecha_cambio__lte=fecha_obj
                )
                .select_related('actuador')  # Evita múltiples consultas por cada actuador
                .only('estado', 'fecha_cambio', 'descripcion', 'actuador__nombre')  # Solo los campos necesarios
                .order_by('-fecha_cambio')[:n_datos]
            )[::-1]  # Invertir para orden cronológico ascendente

            data = [{
                'actuador': h.actuador.nombre,
                'estado': h.estado,
                'fecha': h.fecha_cambio,
                'descripcion': h.descripcion
            } for h in historial]

            return Response({'historial': data}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': f'Ocurrió un error inesperado: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class HistorialRangoDatosSensor(APIView):
    def get(self, request, id, fecha, n_datos):
        # Validación rápida de fecha
        fecha_obj = parse_datetime(fecha)
        if not fecha_obj:
            return Response({'error': 'Formato de fecha inválido.'}, status=status.HTTP_400_BAD_REQUEST)

        if is_naive(fecha_obj):
            fecha_obj = make_aware(fecha_obj)

        try:
            n_datos = int(n_datos)
        except ValueError:
            return Response({'error': 'n_datos debe ser un número entero.'}, status=status.HTTP_400_BAD_REQUEST)

        # Optimización clave: usar .select_related para evitar consultas N+1
        historial_qs = (
            HistorialActuador.objects
            .select_related('actuador')  # Carga el nombre del actuador en el mismo query
            .filter(actuador_id=id, fecha_cambio__lte=fecha_obj)
            .order_by('-fecha_cambio')
            .only('estado', 'fecha_cambio', 'descripcion', 'actuador__nombre')  # Solo los campos necesarios
        )[:n_datos]  # slicing al final para eficiencia

        # Generar respuesta
        data = [
            {
                'actuador': h.actuador.nombre,
                'estado': h.estado,
                'fecha': h.fecha_cambio,
                'descripcion': h.descripcion
            }
            for h in reversed(historial_qs)  # De más antiguo a reciente
        ]

        return Response({'historial': data}, status=status.HTTP_200_OK)
