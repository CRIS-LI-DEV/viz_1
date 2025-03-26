from rest_framework import serializers
from  .models import *
class DatosSensorSerializer(serializers.Serializer):
    boton = serializers.IntegerField()
    puerta = serializers.IntegerField()
    nivel_pozo = serializers.FloatField()
    nivel_pera = serializers.FloatField()
    corriente = serializers.FloatField()
    voltaje = serializers.FloatField()




class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = '__all__'


class ControladorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Controlador
        fields = '__all__'




class HistorialSensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistorialSensor
        fields = ['id', 'sensor', 'valor', 'fecha_cambio']
