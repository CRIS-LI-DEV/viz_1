
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404
from app.models import ControlWebActuador, ControlWebControlador
from app.serializers import ControlWebActuadorSerializer


class ControlWebAPIView(APIView):


    def post(self, request):

        estado_cwc= request.data['cwc']
        estado_cwa_1 = request.data['cwa_1']
        estado_cwa_2 = request.data['cwa_2']



        cwc = ControlWebControlador.objects.get(id = 7)
        cwc.estado = estado_cwc
        cwc.save()
   
        cwa_1= ControlWebActuador.objects.get(id=5) 
        cwa_1.estado = estado_cwa_1
        cwa_1.save()


        cwa_2= ControlWebActuador.objects.get(id=6)
        cwa_2.estado = estado_cwa_2
        cwa_2.save()

        return Response({"mesake":"todo ok"}, status=status.HTTP_200_OK)
        