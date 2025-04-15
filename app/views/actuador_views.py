from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from app.serializers import ActuadorSerializer, HistorialActuadorSerializer,ControlWebActuadorSerializer
from app.models import Actuador
from app.models import HistorialActuador,  ControlWebActuador
from app.services.actuador_service import get_historial_actuador
from rest_framework import status
from rest_framework.generics import get_object_or_404

class ActuadorAPIView(APIView):
    def post(self, request):
        actuador_serializer = ActuadorSerializer(data=request.data)
        if actuador_serializer.is_valid():
            actuador = actuador_serializer.save()
      
            control_web_actuador = ControlWebActuador.objects.create(
                actuador=actuador,
                estado=False  
            )         
            control_web_serializer = ControlWebActuadorSerializer(control_web_actuador)

           
            return Response({
                'actuador': actuador_serializer.data,
                'control_web_actuador': control_web_serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response(actuador_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ActuadorDetalleAPIView(APIView):
    def get(self, request, pk):
        actuador = get_object_or_404(Actuador, id=pk)
        serializer = ActuadorSerializer(actuador)
        return Response(serializer.data, status=status.HTTP_200_OK)