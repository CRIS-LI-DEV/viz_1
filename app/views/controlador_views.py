# views/controlador_views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from app.serializers import ControladorSerializer
from app.models import Controlador, ControlWebControlador
from rest_framework.generics import get_object_or_404


class ControladorAPIView(APIView):

    def get(self, request):
        controlador_id = request.query_params.get('id')
        if controlador_id:
            try:
                controlador = Controlador.objects.get(pk=controlador_id)
                controlador_data = ControladorSerializer(controlador).data
                return Response(controlador_data)
            except Controlador.DoesNotExist:
                return Response({'error': 'Controlador no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        controladores = Controlador.objects.all()
        data = [ControladorSerializer(controlador).data for controlador in controladores]
        return Response(data)

    def post(self, request):
        serializer = ControladorSerializer(data=request.data)
        if serializer.is_valid():
            controlador = serializer.save()
            
            # Crear el objeto ControlWebControlador con estado por defecto (ej. False)
            ControlWebControlador.objects.create(controlador=controlador, estado=False)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ControladorDetalleAPIView(APIView):
    def get(self, request, pk):
        controlador = get_object_or_404(Controlador, id=pk)
        
        cwc = ControlWebControlador.objects.get(controlador_id = pk) 
        
        serializer = ControladorSerializer(controlador)
        return Response({"controlador":serializer.data,"cwc":cwc.estado}, status=status.HTTP_200_OK)