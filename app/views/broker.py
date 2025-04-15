from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from app.models import ControlWebControlador, Actuador,ControlWebActuador, HistorialActuador,Sensor,HistorialSensor

import json



class BrokerIn(APIView):
    def get(self, request):
      
       

        cwc = ControlWebControlador.objects.get(id = 7)

        cwa_1= ControlWebActuador.objects.get(id=4) 
        cwa_2= ControlWebActuador.objects.get(id=5) 
     
       
        return Response({"cwa":cwc.estado,"cwa_1":cwa_1.estado,"cwa_2":cwa_2.estado})
    def post(self, request):
            datos = request.data 

            for clave, valor in datos.items():
                if clave.startswith("a"): 
                    try:
                        solo_numero = int(clave[1:])  
                        actuador_obj = Actuador.objects.get(id=solo_numero)

                     
                        HistorialActuador.objects.create(
                            actuador=actuador_obj,
                            estado=valor,
                            descripcion=""
                        )

                        print(f"Actuador {clave} => Valor: {valor}")

                    except Actuador.DoesNotExist:
                        print(f"⚠️ Actuador con ID {solo_numero} no encontrado.")
                    except ValueError:
                        print(f"⚠️ No se pudo convertir {clave} a número.")
                
            


            for clave, valor in datos.items():
                if clave.startswith("s"): 
                    try:
                        solo_numero = int(clave[1:])  
                        sensor_obj = Sensor.objects.get(id=solo_numero)

                     
                        HistorialSensor.objects.create(
                            sensor=sensor_obj,
                            valor=valor
                 
                        )

                        print(f"Sensor {clave} => Valor: {valor}")

                    except Sensor.DoesNotExist:
                        print(f"⚠️ Actuador con ID {solo_numero} no encontrado.")
                    except ValueError:
                        print(f"⚠️ No se pudo convertir {clave} a número.")
            
            return Response({"mensaje": "Datos procesados correctamente"}, status=status.HTTP_201_CREATED)

class BrokerOut(APIView):
    def get(self, request):
        pass
    def post(self, request):
        
        cwc = ControlWebControlador.objects.get(id = 7)

        cwa_1= ControlWebActuador.objects.get(id=5) 
        cwa_2= ControlWebActuador.objects.get(id=6) 

        
        
        return Response({"cwc":cwc.estado,"cwa_1":cwa_1.estado,"cwa_2":cwa_2.estado})
    
