from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from app.serializers import HistorialSensorSerializer, SensorSerializer
from app.models import HistorialSensor,Sensor
from app.services.sensor_service import get_historial_sensor
from rest_framework.generics import get_object_or_404

class SensorAPIView(APIView):
    def get(self, request):
        sensores = Sensor.objects.all()
        serializer = SensorSerializer(sensores, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
      
        sensor_serializer = SensorSerializer(data=request.data)

        if sensor_serializer.is_valid():
 
            sensor = sensor_serializer.save()

            return Response({
                'sensor': sensor_serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response(sensor_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SensorDetalleAPIView(APIView):
    def get(self, request, pk):
        sensor = get_object_or_404(Sensor, id=pk)
        serializer = SensorSerializer(sensor)
        return Response(serializer.data, status=status.HTTP_200_OK)