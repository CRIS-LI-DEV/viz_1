# views/historial_views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware, is_naive
from django.db.models import Avg, IntegerField
from django.db.models.functions import Cast
from datetime import datetime, timedelta

from app.models import HistorialActuador, HistorialSensor
from app.serializers import HistorialActuadorSerializer, HistorialSensorSerializer



class FiltrarHistorialSensorConResumenAPIView(APIView):
    def post(self, request, registro_id):
        #print("entre")
        fecha_inicio_str = request.data.get('fecha_inicio')
        fecha_final_str = request.data.get('fecha_final')
        numero_resumen = request.data.get('numero_de_resumen')

        # Validación de parámetros
        if not all([fecha_inicio_str, fecha_final_str, numero_resumen]):
            return Response(
                {'error': 'Se requieren fecha_inicio, fecha_final y numero_de_resumen.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            fecha_inicio = parse_datetime(fecha_inicio_str)
            fecha_final = parse_datetime(fecha_final_str)
            numero_resumen = int(numero_resumen)

            if numero_resumen <= 0:
                raise ValueError("numero_de_resumen debe ser mayor que 0")
        except Exception as e:
            return Response({'error': f'Datos inválidos: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

        # Obtener datos del historial en el rango
        historial_qs = HistorialSensor.objects.filter(
            sensor_id=registro_id,
            fecha_cambio__range=(fecha_inicio, fecha_final)
        ).only('valor', 'fecha_cambio').order_by('fecha_cambio')

        if not historial_qs.exists():
            return Response({'error': 'No hay datos en el rango indicado.'}, status=status.HTTP_404_NOT_FOUND)

        # Calcular intervalos
        intervalo = (fecha_final - fecha_inicio) / numero_resumen
        resumen = []

        for i in range(numero_resumen):
            inicio = fecha_inicio + i * intervalo
            fin = inicio + intervalo
            fecha_medio = inicio + (intervalo / 2)

            promedio = historial_qs.filter(
                fecha_cambio__range=(inicio, fin)
            ).aggregate(promedio=Avg('valor'))['promedio'] or 0

            resumen.append({
                'fecha_inicio': inicio,
                'fecha_medio': fecha_medio,
                'fecha_fin': fin,
                'valor_promedio': promedio,
            })

        # Obtener valor inicial antes o igual a la fecha de inicio
        estado_inicio = HistorialSensor.objects.filter(
            sensor_id=registro_id,
            fecha_cambio__lte=fecha_inicio
        ).order_by('-fecha_cambio').only('valor').first()
        valor_inicio = estado_inicio.valor if estado_inicio else 0

        # Obtener valor final antes o igual a la fecha final
        estado_final = HistorialSensor.objects.filter(
            sensor_id=registro_id,
            fecha_cambio__lte=fecha_final
        ).order_by('-fecha_cambio').only('valor').first()
        valor_final = estado_final.valor if estado_final else 0

        return Response({
            'valor_inicio': valor_inicio,
            'valor_final': valor_final,
            'intervalos': resumen
        }, status=status.HTTP_200_OK)
    
    
class FiltrarHistorialActuadorConResumenAPIView(APIView):
    def post(self, request, registro_id):
        # Obtener parámetros
        fecha_inicio_str = request.data.get('fecha_inicio')
        fecha_final_str = request.data.get('fecha_final')
        numero_resumen = request.data.get('numero_de_resumen')

        # Validar que existan
        if not all([fecha_inicio_str, fecha_final_str, numero_resumen]):
            return Response(
                {'error': 'Se requieren fecha_inicio, fecha_final y numero_de_resumen.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        print("PUNTO" , fecha_inicio_str, fecha_final_str, numero_resumen)
        # Parsear fechas y número de resumen
        try:
            fecha_inicio = parse_datetime(fecha_inicio_str)
            fecha_final = parse_datetime(fecha_final_str)
            numero_resumen = int(numero_resumen)
            if fecha_inicio is None or fecha_final is None:
                raise ValueError("Fechas inválidas")
            if numero_resumen <= 0:
                raise ValueError("numero_de_resumen debe ser mayor que 0")
        except Exception as e:
            return Response({'error': f'Datos inválidos: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
        print("PUNTO 2 " , fecha_inicio_str, fecha_final_str, numero_resumen)
        # Aquí ya puedes usar fecha_inicio y fecha_final sin problemas
        historial_qs = HistorialActuador.objects.filter(
            actuador_id=registro_id,
            fecha_cambio__range=(fecha_inicio, fecha_final)
        ).only('estado', 'fecha_cambio').order_by('fecha_cambio')

        if not historial_qs.exists():
            return Response({'error': 'No hay datos en el rango indicado.'}, status=status.HTTP_404_NOT_FOUND)

        intervalo = (fecha_final - fecha_inicio) / numero_resumen
        resumen = []
        print("PUNTO 3 " , historial_qs)
        for i in range(numero_resumen):
            inicio = fecha_inicio + i * intervalo
            fin = inicio + intervalo
            fecha_medio = inicio + (intervalo / 2)

            promedio_estado = historial_qs.filter(
                fecha_cambio__range=(inicio, fin)
            ).annotate(
                estado_int=Cast('estado', IntegerField())
            ).aggregate(
                promedio=Avg('estado_int')
            )['promedio'] or 0

            resumen.append({
                'fecha_inicio': inicio,
                'fecha_medio': fecha_medio,
                'fecha_fin': fin,
                'estado_promedio': promedio_estado,
            })

        estado_inicio = HistorialActuador.objects.filter(
            actuador_id=registro_id,
            fecha_cambio__lte=fecha_inicio
        ).order_by('-fecha_cambio').only('estado').first()
        valor_inicio = estado_inicio.estado if estado_inicio else False

        estado_final = HistorialActuador.objects.filter(
            actuador_id=registro_id,
            fecha_cambio__lte=fecha_final
        ).order_by('-fecha_cambio').only('estado').first()
        valor_final = estado_final.estado if estado_final else False

        return Response({
            'estado_inicio': valor_inicio,
            'estado_final': valor_final,
            'intervalos': resumen
        }, status=status.HTTP_200_OK)
# class FiltrarHistorialActuadorConResumenAPIView(APIView):
#     def post(self, request, registro_id):
#         fecha_inicio = request.data.get('fecha_inicio')
#         fecha_fin = request.data.get('fecha_fin')
#         numero_de_resumen = request.data.get('numero_de_resumen')

#         if not fecha_inicio or not fecha_fin or not numero_de_resumen:
#             return Response({
#                 "error": "Debe proporcionar 'fecha_inicio', 'fecha_fin' y 'numero_de_resumen'."
#             }, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             fecha_inicio = datetime.fromisoformat(fecha_inicio)
#             fecha_fin = datetime.fromisoformat(fecha_fin)
#             numero_de_resumen = int(numero_de_resumen)
#             if numero_de_resumen <= 0:
#                 raise ValueError("numero_de_resumen debe ser positivo.")
#         except ValueError as e:
#             return Response({"error": f"Error en los datos: {str(e)}"},
#                             status=status.HTTP_400_BAD_REQUEST)

#         # Obtener registros del historial del actuador
#         registros = HistorialActuador.objects.filter(
#             actuador_id=registro_id,
#             fecha_cambio__range=(fecha_inicio, fecha_fin)
#         ).order_by('fecha_cambio')

#         total_datos = registros.count()
#         if total_datos == 0:
#             return Response({"error": "No se encontraron datos para el filtro."},
#                             status=status.HTTP_404_NOT_FOUND)

#         tamaño_intervalo = max(total_datos // numero_de_resumen, 1)

#         resumenes = []
#         estados = list(registros.values_list('estado', flat=True))  # Usar 'estado' en lugar de 'valor'
#         fechas = list(registros.values_list('fecha_cambio', flat=True))

#         for i in range(0, total_datos, tamaño_intervalo):
#             grupo_estados = estados[i:i + tamaño_intervalo]
#             grupo_fechas = fechas[i:i + tamaño_intervalo]

#             promedio = sum(grupo_estados) / len(grupo_estados)  # Convertirá True/False en 1/0 automáticamente
#             resumenes.append({
#                 "fecha_inicio": grupo_fechas[0],
#                 "fecha_fin": grupo_fechas[-1],
#                 "promedio_estado": promedio,
#                 "cantidad_datos": len(grupo_estados),
#             })

#         return Response({
#             "total_datos": total_datos,
#             "numero_de_resumen": numero_de_resumen,
#             "tamaño_intervalo": tamaño_intervalo,
#             "resumen": resumenes
#         })

class FiltrarHistorialSensorPorFechasAPIView(APIView):
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
    
class FiltrarHistorialActuadorPorFechasAPIView(APIView):
    def post(self, request, registro_id):
        fecha_ingreso = request.data.get('fecha_inicio')
        fecha_salida = request.data.get('fecha_fin')

        if not fecha_ingreso or not fecha_salida:
            return Response({"error": "Debe proporcionar 'fecha_inicio' y 'fecha_fin'."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            fecha_ingreso = datetime.fromisoformat(fecha_ingreso)
            fecha_salida = datetime.fromisoformat(fecha_salida)
        except ValueError:
            return Response({"error": "Formato de fecha inválido. Use YYYY-MM-DD o YYYY-MM-DDTHH:MM:SS"},
                            status=status.HTTP_400_BAD_REQUEST)

        registros = HistorialActuador.objects.filter(
            actuador_id=registro_id,
            fecha_cambio__range=(fecha_ingreso, fecha_salida)
        )

        serializer = HistorialActuadorSerializer(registros, many=True)
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