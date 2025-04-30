from rest_framework.permissions import BasePermission
from .models import PerfilBasico, PerfilAvanzado

class EsPerfilBasico(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and PerfilBasico.objects.filter(usuario=request.user).exists()

class EsPerfilAvanzado(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and PerfilAvanzado.objects.filter(usuario=request.user).exists()
