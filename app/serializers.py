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



class ControlWebControladorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ControlWebControlador
        fields = ['controlador', 'estado']


class ActuadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actuador
        fields = ['id', 'nombre', 'tipo', 'controlador']  # Incluye los campos relevantes

class ControladorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Controlador
        fields = ['id', 'nombre', 'modelo']  # Incluye los campos relevantes

class ActuadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actuador
        fields = ['id', 'nombre', 'tipo', 'estado', 'fecha_registro', 'controlador']


class ControlWebActuadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ControlWebActuador
        fields = ['id', 'actuador', 'estado']

class HistorialActuadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistorialActuador
        fields = '__all__'