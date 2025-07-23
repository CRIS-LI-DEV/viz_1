# views/historial_views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from app.models import HistorialActuador, HistorialSensor
from app.serializers import HistorialActuadorSerializer, HistorialSensorSerializer
from django.utils.dateparse import parse_datetime
from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware, is_naive
from rest_framework import status
from app.models import HistorialSensor
from app.serializers import HistorialSensorSerializer
from datetime import datetime


class FiltrarHistorialConResumenAPIView(APIView):
    def post(self, request, registro_id):
        fecha_inicio = request.data.get('fecha_inicio')
        fecha_fin = request.data.get('fecha_fin')
        numero_de_resumen = request.data.get('numero_de_resumen')

        if not fecha_inicio or not fecha_fin or not numero_de_resumen:
            return Response({"error": "Debe proporcionar 'fecha_inicio', 'fecha_fin' y 'numero_de_resumen'."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            fecha_inicio = datetime.fromisoformat(fecha_inicio)
            fecha_fin = datetime.fromisoformat(fecha_fin)
            numero_de_resumen = int(numero_de_resumen)
            if numero_de_resumen <= 0:
                raise ValueError("numero_de_resumen debe ser positivo.")
        except ValueError as e:
            return Response({"error": f"Error en los datos: {str(e)}"},
                            status=status.HTTP_400_BAD_REQUEST)

        # Obtener todos los registros filtrados
        registros = HistorialSensor.objects.filter(
            sensor_id=registro_id,
            fecha_cambio__range=(fecha_inicio, fecha_fin)
        ).order_by('fecha_cambio')

        total_datos = registros.count()
        if total_datos == 0:
            return Response({"error": "No se encontraron datos para el filtro."},
                            status=status.HTTP_404_NOT_FOUND)

        # Calcular tamaño del intervalo (número de datos por grupo)
        tamaño_intervalo = max(total_datos // numero_de_resumen, 1)

        resumenes = []
        valores = list(registros.values_list('valor', flat=True))
        fechas = list(registros.values_list('fecha_cambio', flat=True))

        for i in range(0, total_datos, tamaño_intervalo):
            grupo_valores = valores[i:i+tamaño_intervalo]
            grupo_fechas = fechas[i:i+tamaño_intervalo]

            promedio = sum(grupo_valores) / len(grupo_valores)
            fecha_inicio_grupo = grupo_fechas[0]
            fecha_fin_grupo = grupo_fechas[-1]

            resumenes.append({
                "fecha_inicio": fecha_inicio_grupo,
                "fecha_fin": fecha_fin_grupo,
                "promedio_valor": promedio,
                "cantidad_datos": len(grupo_valores),
            })

        return Response({
            "total_datos": total_datos,
            "numero_de_resumen": numero_de_resumen,
            "tamaño_intervalo": tamaño_intervalo,
            "resumen": resumenes
        })

class FiltrarHistorialPorFechasAPIView(APIView):
    def post(self, request, registro_id):
        fecha_ingreso = request.data.get('fecha_inicio')
        fecha_salida = request.data.get('fecha_fin')


        if not fecha_ingreso or not fecha_salida:
            return Response({"error": "Debe proporcionar 'fecha_ingreso' y 'fecha_salida'."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            fecha_ingreso = datetime.fromisoformat(fecha_ingreso)
            fecha_salida = datetime.fromisoformat(fecha_salida)
        except ValueError:
            return Response({"error": "Formato de fecha inválido. Use YYYY-MM-DD o YYYY-MM-DDTHH:MM:SS"},
                            status=status.HTTP_400_BAD_REQUEST)

        # Filtra por registro_id y rango de fechas (ajusta campo según tu modelo)
        registros = HistorialSensor.objects.filter(
            sensor_id=registro_id,
            fecha_cambio__range=(fecha_ingreso, fecha_salida)
        )

        serializer = HistorialSensorSerializer(registros, many=True)
        return Response(serializer.data)
    


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


"""
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
"""

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

        # Consultar historial de sensor en vez de actuador
        historial_qs = (
            HistorialSensor.objects
            .select_related('sensor')  # Cargar el sensor para obtener su nombre y unidad
            .filter(sensor_id=id, fecha_cambio__lte=fecha_obj)
            .order_by('-fecha_cambio')
            .only('valor', 'fecha_cambio', 'sensor__nombre', 'sensor__unidad_medida')  # Solo campos necesarios
        )[:n_datos]  # Limitar la consulta

        # Generar respuesta, ordenando de más antiguo a más reciente
        data = [
            {
                'sensor': h.sensor.nombre,
                'valor': h.valor,
                'unidad_medida': h.sensor.unidad_medida,
                'fecha': h.fecha_cambio
            }
            for h in reversed(historial_qs)
        ]

        return Response({'historial': data}, status=status.HTTP_200_OK)