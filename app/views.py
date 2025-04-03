from django.shortcuts import render, redirect
from .forms import ControladorForm,ActuadorForm,SensorForm
from .models import *
from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from datetime import datetime
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import DatosSensorSerializer

from rest_framework import viewsets
from .models import Sensor
from .serializers import SensorSerializer
from .serializers import ControladorSerializer

from .serializers import HistorialSensorSerializer
def crear_controlador(request):
    if request.method == 'POST':
        controlador = Controlador()
        controlador.nombre = request.POST.get('nombre')
        controlador.modelo = request.POST.get('modelo')
        controlador.save()

        ctrl_web_controlador = ControlWebControlador()
        ctrl_web_controlador.controlador=controlador
        ctrl_web_controlador.estado=False
        ctrl_web_controlador.save()


    else:
        form = ControladorForm()
    return render(request, 'crear_controlador.html', {'form': form})




def crear_sensor(request):
    if request.method == "POST":
        sensor = Sensor()
        sensor.nombre = request.POST.get('nombre')
        sensor.tipo = request.POST.get('tipo')
        controlador_id = request.POST.get('controlador')  # ID del controlador
        controlador = get_object_or_404(Controlador, id=controlador_id)
        sensor.controlador = controlador
        sensor.valor_actual= 0
        sensor.save()
        print(request.POST)
        print("entre")
        print(request.POST.get("nombre"))



        hist_sensor = HistorialSensor()
        hist_sensor.sensor = sensor
        hist_sensor.valor = 0
        hist_sensor.save()
        return HttpResponse("entre")

    
    else:
        form = SensorForm()
        form.fields['controlador'].queryset = Controlador.objects.all()  # Se establece aquí

    return render(request, 'crear_sensor.html', {'form': form})





def crear_actuador(request):
    if request.method == "POST":
        actuador = Actuador()
        actuador.nombre = request.POST.get("nombre")
        actuador.tipo = request.POST.get("tipo")
    
        controlador_id = request.POST.get('controlador')  # ID del controlador
        controlador = get_object_or_404(Controlador, id=controlador_id)

        actuador.controlador = controlador
        actuador.save()  

        hist_actuador = HistorialActuador()
        hist_actuador.actuador = actuador
        hist_actuador.estado= False
        hist_actuador.descripcion=""
       
        hist_actuador.save()

        ctrl_web_actuador= ControlWebActuador()
        ctrl_web_actuador.actuador= actuador
        ctrl_web_actuador.estado= False;
        ctrl_web_actuador.save()




        print(request.POST)
        print("entre")
        print(request.POST.get("nombre"))
        return HttpResponse("entre")
       


       

       
            
    else:
        form = ActuadorForm()
        form.fields['controlador'].queryset = Controlador.objects.all()  # Se asigna en la vista

    return render(request, 'crear_actuador.html', {'form': form})






# Vista para listar controladores
def lista_controladores(request):
    controladores = Controlador.objects.all()
    return render(request, 'lista_controladores.html', {'controladores': controladores})


# Vista para listar sensores
def lista_sensores(request):
    sensores = Sensor.objects.all()
    return render(request, 'lista_sensores.html', {'sensores': sensores})


# Vista para listar actuadores
def lista_actuadores(request):
    actuadores = Actuador.objects.all()
    return render(request, 'lista_actuadores.html', {'actuadores': actuadores})



"""

class recibir(APIView):
    def post(self, request):
        # Imprimir los datos que llegan
        print("Datos recibidos:", request.data)
        sensores = request.data['sensores']
        for x in sensores:
            print(f" Sensor: {x['id']}, Valor: {x['valor']}")

            sensor = request.data['sensores'][0]
            sensor_id = x['id']
            sensor_valor = x['valor']


       

            sensor = Sensor.objects.get(id=sensor_id)
            sensor.valor_actual=sensor_valor
            sensor.save()
            historial = HistorialSensor(
            sensor=sensor,
            valor=sensor_valor,  # Valor que quieres registrar
            fecha_cambio=datetime.now()  # Puedes usar la fecha actual o cualquier otra
            )

# Guardar el registro
            historial.save()

       

        # Procesar los datos con el serializador
        serializer = DatosSensorSerializer(data=request.data)
        if serializer.is_valid():
            return Response({"status": "success", "received_data": serializer.validated_data}, status=status.HTTP_200_OK)
        
        return Response({"status": "error", "message": "JSON inválido", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    




"""

class recibir(APIView):
    def post(self, request):
        # Imprimir los datos que llegan
        print("Datos recibidos:", request.data)
        
        # Procesar sensores
        sensores = request.data.get('sensores', [])
        for x in sensores:
            print(f" Sensor: {x['id']}, Valor: {x['valor']}")

            sensor_id = x['id']
            sensor_valor = x['valor']

            try:
                sensor = Sensor.objects.get(id=sensor_id)
                sensor.valor_actual = sensor_valor
                sensor.save()

                historial = HistorialSensor(
                    sensor=sensor,
                    valor=sensor_valor,
                    fecha_cambio=datetime.now()
                )
                historial.save()
            except Sensor.DoesNotExist:
                print(f"Sensor con ID {sensor_id} no encontrado.")

        # Procesar actuadores
        actuadores = request.data.get('actuadores', [])
        for x in actuadores:
            print(f" Actuador: {x['id']}, Estado: {x['estado']}")

            actuador_id = x['id']
            actuador_estado = x['estado']

            try:
                actuador = Actuador.objects.get(id=actuador_id)
                actuador.estado = bool(actuador_estado)  # Convertir estado a booleano
                actuador.save()

                historial = HistorialActuador(
                    actuador=actuador,
                    estado=actuador.estado,
                    fecha_cambio=datetime.now()
                )
                historial.save()
            except Actuador.DoesNotExist:
                print(f"Actuador con ID {actuador_id} no encontrado.")

        # Procesar los datos con el serializador
        serializer = DatosSensorSerializer(data=request.data)
        if serializer.is_valid():
            return Response({"status": "success", "received_data": serializer.validated_data}, status=status.HTTP_200_OK)
        
        return Response({"status": "error", "message": "JSON inválido", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)







# Vista para mostrar los detalles de un controlador específico
def detalle_controlador(request, controlador_id):
    controlador = Controlador.objects.get(id=controlador_id)  # Obtener un controlador por su id
    sensores = Sensor.objects.filter(controlador=controlador)  # Obtener los sensores asociados a este controlador
    actuadores = Actuador.objects.filter(controlador=controlador)  # Obtener los actuadores asociados a este controlador
    return render(request, 'detalle_controlador.html', {
        'controlador': controlador,
        'sensores': sensores,
        'actuadores': actuadores,
    })

# Vista para mostrar todos los sensores

# Vista para mostrar los detalles de un sensor específico
def detalle_sensor(request, sensor_id):
    sensor = Sensor.objects.get(id=sensor_id)  # Obtener un sensor por su id
    historial = HistorialSensor.objects.filter(sensor=sensor)  # Obtener el historial de un sensor
    return render(request, 'detalle_sensor.html', {
        'sensor': sensor,
        'historial': historial,
    })

# Vista para mostrar todos los actuadores


# Vista para mostrar los detalles de un actuador específico
def detalle_actuador(request, actuador_id):
    actuador = Actuador.objects.get(id=actuador_id)  # Obtener un actuador por su id
    historial = HistorialActuador.objects.filter(actuador=actuador)  # Obtener el historial de un actuador
    return render(request, 'detalle_actuador.html', {
        'actuador': actuador,
        'historial': historial,
    })








def detalle_historial_sensor(request, sensor_id):
    try:
        # Filtrar los historiales para un sensor específico
        historiales = HistorialSensor.objects.filter(sensor_id=sensor_id).order_by('-fecha_cambio')[:100]
        fechas = [historial.fecha_cambio.strftime('%Y-%m-%d %H:%M:%S') for historial in historiales]  # Formato de fecha
        valores = [historial.valor for historial in historiales]  # Asumiendo que 'valor' es el campo con el dato
        sensor = Sensor.objects.get(id=sensor_id)
        
        return render(request, 'historial_sensor.html', {
            'fechas': fechas,
            'valores': valores,
            'nombre':sensor.nombre            
        })
    
        print(historiales)

        return render(request, 'historial_sensor.html', {'historiales': historiales})
    
    except HistorialSensor.DoesNotExist:
        return render(request, 'historial_sensor.html', {'error': 'No se encontraron historiales para este sensor.'})



def detalle_historial_actuador(request, actuador_id):
    try:
        # Filtrar los historiales para un actuador específico
        historiales = HistorialActuador.objects.filter(actuador_id=actuador_id).order_by('-fecha_cambio')[:100]
        
        # Crear listas de fechas y estados para mostrar en la plantilla
        fechas = [historial.fecha_cambio.strftime('%Y-%m-%d %H:%M:%S') for historial in historiales]  # Formato de fecha
        estados = [1 if historial.estado else 0 for historial in historiales]  # Estado como texto
        actuador = Actuador.objects.get(id=actuador_id)
        print(estados)
        return render(request, 'historial_actuador.html', {
            'fechas': fechas,
            'estados': estados,
            'nombre': actuador.nombre
        })
    
    except HistorialActuador.DoesNotExist:
        return render(request, 'historial_actuador.html', {'error': 'No se encontraron historiales para este actuador.'})



@api_view(['GET'])
def listar_sensores(request):
    sensores = Sensor.objects.all()
    serializer = SensorSerializer(sensores, many=True)
    return Response(serializer.data)




# Vista basada en función para listar controladores
@api_view(['GET'])
def listar_controladores(request):
    controladores = Controlador.objects.all()
    serializer = ControladorSerializer(controladores, many=True)
    return Response(serializer.data)


# @api_view(['GET'])
# def listar_historial_sensor(request, sensor_id):
#     historial = HistorialSensor.objects.filter(sensor_id=sensor_id)
#     serializer = HistorialSensorSerializer(historial, many=True)
#     return Response(serializer.data)



@api_view(['GET'])
def listar_historial_sensor(request, sensor_id):
    historial = HistorialSensor.objects.filter(sensor_id=sensor_id).order_by('-id')[:100]
    serializer = HistorialSensorSerializer(historial, many=True)
    return Response(serializer.data)
