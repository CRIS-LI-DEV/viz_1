from django.db import models
from django.contrib.auth.models import User


# Modelo para usuario relacionado con el usuario de Django
class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} - {self.telefono}'  # Cambié 'direccion' por 'telefono'


# Modelo para el controlador
class Controlador(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    modelo = models.CharField(max_length=100, blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre


# Modelo de relación para controlar un controlador desde la web
class ControlWebControlador(models.Model):
    controlador = models.ForeignKey('Controlador', on_delete=models.CASCADE)
    estado = models.BooleanField()

# Modelo para el sensor
class Sensor(models.Model):
    TIPO_CHOICES = [
        ('NIVEL-ULTRASONICO', 'NIVEL-ULTRASONICO'),
        ('NIVEL-PERA', 'NIVEL-PERA'),
        ('CAUDAL', 'CAUDAL'),
        ('CA', 'CA'),
        ('CC', 'CC'),
        ('VA', 'VA'),
        ('VC', 'VC'),
        ('SWITCH','SWITCH')
    ]

    nombre = models.CharField(max_length=100, unique=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    unidad_medida = models.CharField(max_length=50, help_text="Ejemplo: °C, %, Pa, lux")
    valor_actual = models.FloatField(default=0.0)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    controlador = models.ForeignKey('Controlador', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre} ({self.tipo} - {self.valor_actual} {self.unidad_medida})"


# Historial de sensores
class HistorialSensor(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    valor = models.FloatField()
    fecha_cambio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Historial de {self.sensor.nombre} - {self.valor} {self.sensor.unidad_medida} en {self.fecha_cambio}"


# Modelo para el actuador
class Actuador(models.Model):
    TIPO_CHOICES = [
        ('RELE', 'RELE'),
        ('ELECTRO-VALVULA', 'ELECTRO-VALVULA'),
    ]

    nombre = models.CharField(max_length=100, unique=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    estado = models.BooleanField(default=False)  # True para activo, False para inactivo
    fecha_registro = models.DateTimeField(auto_now_add=True)
    controlador = models.ForeignKey('Controlador', on_delete=models.CASCADE)

    def __str__(self):
        estado_str = "Activo" if self.estado else "Inactivo"
        return f"{self.nombre} ({self.tipo} - {estado_str})"


# Historial de actuadores
class HistorialActuador(models.Model):
    actuador = models.ForeignKey(Actuador, on_delete=models.CASCADE)
    estado = models.BooleanField()  # Estado que tenía el actuador en el momento del historial
    fecha_cambio = models.DateTimeField(auto_now_add=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        estado_str = "Activo" if self.estado else "Inactivo"
        return f"Historial de {self.actuador.nombre} - {estado_str} en {self.fecha_cambio}"


# Control web para actuador (modelo corregido)
class ControlWebActuador(models.Model):
    actuador = models.ForeignKey('Actuador', on_delete=models.CASCADE)
    estado = models.BooleanField()








class PerfilAvanzado(models.Model):      
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)


class PerfilBasico(models.Model):   
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    
 