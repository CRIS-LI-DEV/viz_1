# urls.py
from django.urls import path
from app.views.actuador_views import  ActuadorAPIView, ActuadorDetalleAPIView
from app.views.historial_views import HistorialActuadorAPIView, HistorialSensorAPIView
from app.views.controlador_views import ControladorAPIView,ControladorDetalleAPIView
from app.views.broker import BrokerIn,BrokerOut
from app.views.sensor_views import SensorAPIView, SensorDetalleAPIView
from app.views.control_web import ControlWebAPIView

historiales = [ 
    path('api/actuador/<int:id>/historial/<int:numero_registros>/', HistorialActuadorAPIView.as_view(), name='historial_actuador'),
    path('api/sensor/<int:id>/historial/<int:numero_registros>/', HistorialSensorAPIView.as_view(), name='historial_actuador')
    ]



broker = [
    path('br-in/', BrokerIn.as_view(), name='broker_in'),
    path('br-out/', BrokerOut.as_view(), name='broker_out')
    ]



controladores = [
    path('api/controladores/', ControladorAPIView.as_view(), name='controlador'),
      path('api/controladores/<int:pk>/', ControladorDetalleAPIView.as_view(), name='controlador')
    ]

actuadores =[
    path('api/actuadores/<int:pk>/', ActuadorDetalleAPIView.as_view(), name='actuador-detalle'),
    path('api/actuadores/', ActuadorAPIView.as_view(), name='actuador-detalle'),
    
    ]

sensores = [ 
    path('api/sensor/', SensorAPIView.as_view(), name='sensor'),
    path('api/sensores/<int:pk>/', SensorDetalleAPIView.as_view(), name='sensor-detalle'),
    ]

control_web=[
    path('api/control_web/', ControlWebAPIView.as_view(), name='control_web'),


]
urlpatterns = historiales + broker + controladores + sensores +actuadores + control_web
