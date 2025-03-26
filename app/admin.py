from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Usuario, Controlador, Sensor, Actuador, HistorialSensor, HistorialActuador, ControlWebControlador, ControlWebActuador


# Registro de Usuario (si necesitas personalizar la vista de usuario en el admin)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('user', 'telefono')  # Campos a mostrar en la lista
    search_fields = ('user__username', 'telefono')  # Campos para búsqueda

admin.site.register(Usuario, UsuarioAdmin)


# Registro de Controlador
class ControladorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'modelo', 'fecha_registro')  # Campos a mostrar en la lista
    search_fields = ('nombre', 'modelo')  # Campos para búsqueda

admin.site.register(Controlador, ControladorAdmin)


# Registro de Sensor
class SensorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo', 'valor_actual', 'unidad_medida', 'controlador', 'fecha_registro')  # Campos a mostrar en la lista
    search_fields = ('nombre', 'tipo')  # Campos para búsqueda

admin.site.register(Sensor, SensorAdmin)


# Registro de Historial de Sensor
class HistorialSensorAdmin(admin.ModelAdmin):
    list_display = ('sensor', 'valor', 'fecha_cambio')  # Campos a mostrar en la lista
    search_fields = ('sensor__nombre',)  # Campos para búsqueda

admin.site.register(HistorialSensor, HistorialSensorAdmin)


# Registro de Actuador
class ActuadorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo', 'estado', 'fecha_registro', 'controlador')  # Campos a mostrar en la lista
    search_fields = ('nombre', 'tipo')  # Campos para búsqueda

admin.site.register(Actuador, ActuadorAdmin)


# Registro de Historial de Actuador
class HistorialActuadorAdmin(admin.ModelAdmin):
    list_display = ('actuador', 'estado', 'fecha_cambio', 'descripcion')  # Campos a mostrar en la lista
    search_fields = ('actuador__nombre',)  # Campos para búsqueda

admin.site.register(HistorialActuador, HistorialActuadorAdmin)


# Registro de ControlWebControlador
class ControlWebControladorAdmin(admin.ModelAdmin):
    list_display = ('controlador', 'estado')  # Campos a mostrar en la lista
    search_fields = ('controlador__nombre',)  # Campos para búsqueda

admin.site.register(ControlWebControlador, ControlWebControladorAdmin)


# Registro de ControlWebActuador
class ControlWebActuadorAdmin(admin.ModelAdmin):
    list_display = ('actuador', 'estado')  # Campos a mostrar en la lista
    search_fields = ('actuador__nombre',)  # Campos para búsqueda

admin.site.register(ControlWebActuador, ControlWebActuadorAdmin)
