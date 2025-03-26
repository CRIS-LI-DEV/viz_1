
from django.contrib import admin
from django.urls import path
from app.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('controlador/', crear_controlador),
    path('sensor/', crear_sensor),
    path('actuador/', crear_actuador),
    path('lista_controladores/', lista_controladores, name='lista_controladores'),
    path('lista_sensores/', lista_sensores, name='lista_sensores'),
    path('lista_actuadores/', lista_actuadores, name='lista_actuadores'),
    path('api/recibir-json/', recibir.as_view()),
    path('controladores/<int:controlador_id>/', detalle_controlador, name='detalle_controlador'),
    path('sensores/<int:sensor_id>/', detalle_sensor, name='detalle_sensor'),
    path('actuadores/<int:actuador_id>/', detalle_actuador, name='detalle_actuador'),
    path('detalle_historial_sensor/<int:sensor_id>/', detalle_historial_sensor),
    path('detalle_historial_actuador/<int:actuador_id>', detalle_historial_actuador, name='detalle_historial_actuador'),
     path('api/sensores/', listar_sensores, name='listar_sensores'),
     path('api/controladores/', listar_controladores, name='listar_controladores'),
      path('api/historial-sensor/<int:sensor_id>/', listar_historial_sensor, name='listar_historial_sensor')
]
