import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils.dateparse import parse_datetime
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.sala = self.scope['url_route']['kwargs']['sala']
        self.sala_grupo = f'chat_{self.sala}'
        await self.channel_layer.group_add(self.sala_grupo, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.sala_grupo, self.channel_name)

    async def receive(self, text_data):
        print("MENSAJE-CLIENTE")
        try:
            data = json.loads(text_data)
            sensor_id = data.get("sensor_id")
            fecha_inicio = parse_datetime(data.get("fecha_inicio"))
            fecha_final = parse_datetime(data.get("fecha_final"))
            numero_resumen = int(data.get("numero_de_resumen"))

            if not all([sensor_id, fecha_inicio, fecha_final, numero_resumen]):
                await self.send_error("Faltan parámetros requeridos.")
                return

            if numero_resumen <= 0:
                await self.send_error("numero_de_resumen debe ser mayor que 0.")
                return

            resultado = await self.calcular_resumen(sensor_id, fecha_inicio, fecha_final, numero_resumen)
            await self.send(text_data=json.dumps(resultado))

        except Exception as e:
            await self.send_error(str(e))

    async def send_error(self, mensaje):
        await self.send(text_data=json.dumps({"error": mensaje}))

    async def chat_mensaje(self, event):
        await self.send(text_data=json.dumps({
            'mensaje': event['mensaje']
        }))

    @database_sync_to_async
    def calcular_resumen(self, sensor_id, fecha_inicio, fecha_final, numero_resumen):
        from .models import HistorialSensor
        import bisect

        datos = list(HistorialSensor.objects.filter(
            sensor_id=sensor_id,
            fecha_cambio__range=(fecha_inicio, fecha_final)
        ).only('valor', 'fecha_cambio').order_by('fecha_cambio').values_list('fecha_cambio', 'valor'))

        if not datos:
            return {'error': 'No hay datos en el rango indicado.'}

        intervalo = (fecha_final - fecha_inicio) / numero_resumen
        resumen = []

        # Crear listas separadas para fechas y valores para búsqueda eficiente
        fechas = [f for f, v in datos]
        valores = [v for f, v in datos]

        for i in range(numero_resumen):
            inicio = fecha_inicio + i * intervalo
            fin = inicio + intervalo
            fecha_medio = inicio + (intervalo / 2)

            # Buscar indices con bisect para limitar el slice de valores en el intervalo
            idx_inicio = bisect.bisect_left(fechas, inicio)
            idx_fin = bisect.bisect_left(fechas, fin)

            valores_en_intervalo = valores[idx_inicio:idx_fin]

            promedio = sum(valores_en_intervalo) / len(valores_en_intervalo) if valores_en_intervalo else 0

            resumen.append({
                'fecha_inicio': inicio.isoformat(),
                'fecha_medio': fecha_medio.isoformat(),
                'fecha_fin': fin.isoformat(),
                'valor_promedio': promedio,
            })

        # Valor inicial (antes o igual a fecha_inicio)
        estado_inicio = HistorialSensor.objects.filter(
            sensor_id=sensor_id,
            fecha_cambio__lte=fecha_inicio
        ).order_by('-fecha_cambio').only('valor').first()
        valor_inicio = estado_inicio.valor if estado_inicio else 0

        # Valor final (antes o igual a fecha_final)
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
