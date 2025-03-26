from django import forms
from .models import Controlador

class ControladorForm(forms.Form):
    nombre = forms.CharField(max_length=100, label='Nombre del Controlador', widget=forms.TextInput(attrs={'placeholder': 'Nombre del controlador'}))
    modelo = forms.CharField(max_length=100, label='Modelo del Controlador', widget=forms.TextInput(attrs={'placeholder': 'Modelo del controlador'}))

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if 'CONTROLADOR' not in nombre:
            raise forms.ValidationError('El nombre debe contener la palabra "CONTROLADOR".')
        return nombre
    

class SensorForm(forms.Form):
    TIPO_CHOICES = [
        ('NIVEL-ULTRASONICO', 'NIVEL-ULTRASONICO'),
        ('NIVEL-PERA', 'NIVEL-PERA'),
        ('CAUDAL', 'CAUDAL'),
        ('CA', 'CA'),
        ('CC', 'CC'),
        ('VA', 'VA'),
        ('VC', 'VC'),
    ]

    nombre = forms.CharField(
        max_length=100, 
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    tipo = forms.ChoiceField(
        choices=TIPO_CHOICES, 
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    unidad_medida = forms.CharField(
        max_length=50, 
        help_text="Ejemplo: °C, %, Pa, lux",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    controlador = forms.ModelChoiceField(
        queryset=Controlador.objects.none(),  
        empty_label="Seleccione un controlador",
        widget=forms.Select(attrs={'class': 'form-control'})
    )




class ActuadorForm(forms.Form):
   
   
    TIPO_CHOICES = [
        ('RELE', 'RELE'),
        ('ELECTRO-VALVULA', 'ELECTRO-VALVULA'),
    ]

    nombre = forms.CharField(
        max_length=100, 
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    tipo = forms.ChoiceField(
        choices=TIPO_CHOICES, 
        widget=forms.Select(attrs={'class': 'form-control'})
    )
   
    controlador = forms.ModelChoiceField(
        queryset=Controlador.objects.none(),  #
        empty_label="Seleccione un controlador",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
