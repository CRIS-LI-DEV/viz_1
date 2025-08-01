import json
from datetime import datetime
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware, is_naive


def safe_serialize(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Tipo no serializable: {type(obj)}")


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.sala = self.scope['url_route']['kwargs']['sala']
        self.sala_grupo = f'chat_{self.sala}'
        await self.channel_layer.group_add(self.sala_grupo, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.sala_grupo, self.channel_name)

    async def receive(self, text_data):
        """
        Espera recibir un JSON con acción y parámetros.
        """
        try:
            data = json.loads(text_data)
            accion = data.get("accion")

            if accion == "filtrar_sensor_resumen":
                sensor_id = data.get("sensor_id")
                fecha_inicio = parse_datetime(data.get("fecha_inicio"))
                fecha_final = parse_datetime(data.get("fecha_final"))
                numero_resumen = int(data.get("numero_de_resumen"))
                resultado = await self.filtrar_historial_sensor_con_resumen(sensor_id, fecha_inicio, fecha_final, numero_resumen)
                await self.send_json(resultado)

            elif accion == "filtrar_actuador_resumen":
                actuador_id = data.get("actuador_id")
                fecha_inicio = parse_datetime(data.get("fecha_inicio"))
                fecha_final = parse_datetime(data.get("fecha_final"))
                numero_resumen = int(data.get("numero_de_resumen"))
                resultado = await self.filtrar_historial_actuador_con_resumen(actuador_id, fecha_inicio, fecha_final, numero_resumen)
                await self.send_json(resultado)

            elif accion == "filtrar_sensor_por_fechas":
                sensor_id = data.get("sensor_id")
                fecha_inicio = parse_datetime(data.get("fecha_inicio"))
                fecha_final = parse_datetime(data.get("fecha_final"))
                resultado = await self.filtrar_historial_sensor_por_fechas(sensor_id, fecha_inicio, fecha_final)
                await self.send_json(resultado)

            elif accion == "filtrar_actuador_por_fechas":
                actuador_id = data.get("actuador_id")
                fecha_inicio = parse_datetime(data.get("fecha_inicio"))
                fecha_final = parse_datetime(data.get("fecha_final"))
                resultado = await self.filtrar_historial_actuador_por_fechas(actuador_id, fecha_inicio, fecha_final)
                await self.send_json(resultado)

            elif accion == "ultimos_n_sensor":
                sensor_id = data.get("sensor_id")
                n = int(data.get("n"))
                resultado = await self.historial_sensor_ultimos_n(sensor_id, n)
                await self.send_json(resultado)

            elif accion == "ultimos_n_actuador":
                actuador_id = data.get("actuador_id")
                n = int(data.get("n"))
                resultado = await self.historial_actuador_ultimos_n(actuador_id, n)
                await self.send_json(resultado)

            elif accion == "rango_datos_sensor":
                sensor_id = data.get("sensor_id")
                fecha_str = data.get("fecha")
                n = int(data.get("n"))
                resultado = await self.historial_rango_datos_sensor(sensor_id, fecha_str, n)
                await self.send_json(resultado)

            elif accion == "rango_datos_actuador":
                actuador_id = data.get("actuador_id")
                fecha_str = data.get("fecha")
                n = int(data.get("n"))
                resultado = await self.historial_rango_datos_actuador(actuador_id, fecha_str, n)
                await self.send_json(resultado)

            else:
                await self.send_error("Acción no reconocida.")

        except Exception as e:
            await self.send_error(f"Error procesando mensaje: {str(e)}")

    async def send_error(self, mensaje):
        await self.send_json({"error": mensaje})

    async def send_json(self, data):
        # Serializa datos con soporte para datetime
        await self.send(text_data=json.dumps(data, default=safe_serialize))

    ##################
    # Funciones async con acceso a BD
    ##################

    @database_sync_to_async
    def filtrar_historial_sensor_con_resumen(self, sensor_id, fecha_inicio, fecha_final, numero_resumen):
        from django.db.models import Avg, IntegerField
        from django.db.models.functions import Cast
        from app.models import HistorialSensor

        if not all([sensor_id, fecha_inicio, fecha_final, numero_resumen]) or numero_resumen <= 0:
            return {"error": "Parámetros inválidos o incompletos."}

        historial_qs = HistorialSensor.objects.filter(
            sensor_id=sensor_id,
            fecha_cambio__range=(fecha_inicio, fecha_final)
        ).only('valor', 'fecha_cambio').order_by('fecha_cambio')

        if not historial_qs.exists():
            return {"error": "No hay datos en el rango indicado."}

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

        estado_inicio = HistorialSensor.objects.filter(
            sensor_id=sensor_id,
            fecha_cambio__lte=fecha_inicio
        ).order_by('-fecha_cambio').only('valor').first()
        valor_inicio = estado_inicio.valor if estado_inicio else 0

        estado_final = HistorialSensor.objects.filter(
            sensor_id=sensor_id,
            fecha_cambio__lte=fecha_final
        ).order_by('-fecha_cambio').only('valor').first()
        valor_final = estado_final.valor if estado_final else 0

        return {
            'valor_inicio': valor_inicio,
            'valor_final': valor_final,
            'intervalos': resumen
        }

    @database_sync_to_async
    def filtrar_historial_actuador_con_resumen(self, actuador_id, fecha_inicio, fecha_final, numero_resumen):
        from django.db.models import Avg, IntegerField
        from django.db.models.functions import Cast
        from app.models import HistorialActuador

        if not all([actuador_id, fecha_inicio, fecha_final, numero_resumen]) or numero_resumen <= 0:
            return {"error": "Parámetros inválidos o incompletos."}

        historial_qs = HistorialActuador.objects.filter(
            actuador_id=actuador_id,
            fecha_cambio__range=(fecha_inicio, fecha_final)
        ).only('estado', 'fecha_cambio').order_by('fecha_cambio')

        if not historial_qs.exists():
            return {"error": "No hay datos en el rango indicado."}

        intervalo = (fecha_final - fecha_inicio) / numero_resumen
        resumen = []

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
            actuador_id=actuador_id,
            fecha_cambio__lte=fecha_inicio
        ).order_by('-fecha_cambio').only('estado').first()
        valor_inicio = estado_inicio.estado if estado_inicio else False

        estado_final = HistorialActuador.objects.filter(
            actuador_id=actuador_id,
            fecha_cambio__lte=fecha_final
        ).order_by('-fecha_cambio').only('estado').first()
        valor_final = estado_final.estado if estado_final else False

        return {
            'estado_inicio': valor_inicio,
            'estado_final': valor_final,
            'intervalos': resumen
        }

    @database_sync_to_async
    def filtrar_historial_sensor_por_fechas(self, sensor_id, fecha_inicio, fecha_final):
        from app.models import HistorialSensor
        if not all([sensor_id, fecha_inicio, fecha_final]):
            return {"error": "Parámetros inválidos o incompletos."}

        registros = HistorialSensor.objects.filter(
            sensor_id=sensor_id,
            fecha_cambio__range=(fecha_inicio, fecha_final)
        ).order_by('fecha_cambio')

        return {
            "registros": list(registros.values('id', 'valor', 'fecha_cambio'))
        }

    @database_sync_to_async
    def filtrar_historial_actuador_por_fechas(self, actuador_id, fecha_inicio, fecha_final):
        from app.models import HistorialActuador
        if not all([actuador_id, fecha_inicio, fecha_final]):
            return {"error": "Parámetros inválidos o incompletos."}

        registros = HistorialActuador.objects.filter(
            actuador_id=actuador_id,
            fecha_cambio__range=(fecha_inicio, fecha_final)
        ).order_by('fecha_cambio')

        return {
            "registros": list(registros.values('id', 'estado', 'fecha_cambio'))
        }

    @database_sync_to_async
    def historial_sensor_ultimos_n(self, sensor_id, n):
        from app.models import HistorialSensor
        if not sensor_id or n <= 0:
            return {"error": "Parámetros inválidos."}

        historial = HistorialSensor.objects.filter(sensor_id=sensor_id).order_by('-fecha_cambio')[:n]
        data = [
            {
                'valor': h.valor,
                'fecha_cambio': h.fecha_cambio
            } for h in reversed(historial)
        ]
        return {"historial": data}

    @database_sync_to_async
    def historial_actuador_ultimos_n(self, actuador_id, n):
        from app.models import HistorialActuador
        if not actuador_id or n <= 0:
            return {"error": "Parámetros inválidos."}

        historial = HistorialActuador.objects.filter(actuador_id=actuador_id).order_by('-fecha_cambio')[:n]
        data = [
            {
                'estado': h.estado,
                'fecha_cambio': h.fecha_cambio
            } for h in reversed(historial)
        ]
        return {"historial": data}

    @database_sync_to_async
    def historial_rango_datos_sensor(self, sensor_id, fecha_str, n):
        from app.models import HistorialSensor
        if not sensor_id or not fecha_str or n <= 0:
            return {"error": "Parámetros inválidos."}

        fecha_obj = parse_datetime(fecha_str)
        if not fecha_obj:
            return {"error": "Formato de fecha inválido."}

        if is_naive(fecha_obj):
            fecha_obj = make_aware(fecha_obj)

        historial_qs = (
            HistorialSensor.objects
            .filter(sensor_id=sensor_id, fecha_cambio__lte=fecha_obj)
            .order_by('-fecha_cambio')
        )[:n]

        data = [
            {
                'valor': h.valor,
                'fecha_cambio': h.fecha_cambio
            } for h in reversed(historial_qs)
        ]
        return {"historial": data}

    @database_sync_to_async
    def historial_rango_datos_actuador(self, actuador_id, fecha_str, n):
        from app.models import HistorialActuador
        if not actuador_id or not fecha_str or n <= 0:
            return {"error": "Parámetros inválidos."}

        fecha_obj = parse_datetime(fecha_str)
        if not fecha_obj:
            return {"error": "Formato de fecha inválido."}

        if is_naive(fecha_obj):
            fecha_obj = make_aware(fecha_obj)

        historial_qs = (
            HistorialActuador.objects
            .filter(actuador_id=actuador_id, fecha_cambio__lte=fecha_obj)
            .order_by('-fecha_cambio')
        )[:n]

        data = [
            {
                'estado': h.estado,
                'fecha_cambio': h.fecha_cambio
            } for h in reversed(historial_qs)
        ]
        return {"historial": data}
