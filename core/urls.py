# urls.py
from django.urls import path
from app.views.actuador_views import  ActuadorAPIView, ActuadorDetalleAPIView
from app.views.historial_views import HistorialActuadorAPIView, HistorialSensorAPIView,HistorialRangoDatosSensor,HistorialRangoDatosActuador, FiltrarHistorialPorFechasAPIView,FiltrarHistorialConResumenAPIView
from app.views.controlador_views import ControladorAPIView,ControladorDetalleAPIView
from app.views.broker import BrokerIn,BrokerOut
from app.views.sensor_views import SensorAPIView, SensorDetalleAPIView
from app.views.control_web import ControlWebAPIView



from app.views.auth_views import *
historiales = [ 
    path('api/actuadores/<int:id>/historial/<int:numero_registros>/', HistorialActuadorAPIView.as_view(), name='historial_actuador'),
    path('api/sensores/<int:id>/historial/<int:numero_registros>/', HistorialSensorAPIView.as_view(), name='historial_sensor'),
    path('api/sensores/<int:id>/fecha/<str:fecha>/n_datos/<int:n_datos>/', HistorialRangoDatosSensor.as_view(), name='historial_fechas_n_datos'),
    path('api/actuadores/<int:id>/fecha/<str:fecha>/n_datos/<int:n_datos>/', HistorialRangoDatosActuador.as_view(), name='historial_fechas_n_datos'),
   path('api/historial/<int:registro_id>/', FiltrarHistorialPorFechasAPIView.as_view(), name='filtrar-historial'),
   path('api/historial/resumen/<int:registro_id>/', FiltrarHistorialConResumenAPIView.as_view(), name='historial-resumen'),

    ]



broker = [
    path('br-in/', BrokerIn.as_view(), name='broker_in'),
    path('br-out/', BrokerOut.as_view(), name='broker_out')
    ]



controladores = [
    path('api/controladores/', ControladorAPIView.as_view(), name='controlador'),
      path('api/controladores/<int:pk>/', ControladorDetalleAPIView.as_view(), name='detalle-controlador')
    ]

actuadores =[
    path('api/actuadores/<int:pk>/', ActuadorDetalleAPIView.as_view(), name='actuador-detalle'),
    path('api/actuadores/', ActuadorAPIView.as_view(), name='actuador'),
    
    ]

sensores = [ 
    path('api/sensores/', SensorAPIView.as_view(), name='sensor'),
    path('api/sensores/<int:pk>/', SensorDetalleAPIView.as_view(), name='sensor-detalle'),
    ]

control_web=[
    path('api/control_web/', ControlWebAPIView.as_view(), name='control_web'),

]

auth_user =[
    path('api/user/register/', Usuario.as_view(), name='registro'),
    path('api/user/login/', login, name='login'),
    path('api/user/test-p-basico/', profile_basico, name='test-perfil-avanzado'), 
    path('api/user/test-p-avanzado/', profile_avanzado, name='test-basico-avanzado'),
]




urlpatterns = historiales + broker + controladores + sensores + actuadores + control_web + auth_user
