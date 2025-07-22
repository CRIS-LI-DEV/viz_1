from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.views import APIView
from django.contrib.auth.models import User, Permission
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from app.models import PerfilAvanzado, PerfilBasico 
from app.serializers import UserSerializers
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from app.permissions import EsPerfilBasico, EsPerfilAvanzado


class   Usuario(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        print("ENTRE")
        nivel_mensaje=""
        username = request.data.get('username')
        password = request.data.get('password')
        nivel = request.data.get('nivel')

        if not username or not password or not nivel:
            return Response({"error": "Se requieren los campos 'username', 'password' y 'nivel'."}, status=status.HTTP_400_BAD_REQUEST)

   
        user = User.objects.create_user(username=username, password=password)
      
        

        token = Token.objects.create(user=user)
        mensaje=""

        if nivel == 'AV':  

            avanzado = PerfilAvanzado(usuario=user)
            avanzado.save()

            mensaje="Usuario avanzado creado"

        elif nivel == 'BA':  
            
            basico = PerfilBasico(usuario = user)
            basico.save()
            mensaje="Usuario basico creado"
        else:
            return Response({"mensaje": "Nivel de usuario no válido."}, status=status.HTTP_400_BAD_REQUEST)

     
        return Response({
            "mensaje": mensaje,
            'token': token.key, 
            "usuario": {
                "username": user.username,
                "password": password
            }
        }, status=status.HTTP_201_CREATED)
    





@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    perfil_avanzado=False
    user = get_object_or_404(User, username=request.data['username'])
    existe = PerfilAvanzado.objects.get(usuario_id=user.id).count()
    print(existe)
    if existe >=1:
        perfil_avanzado=True
    else:
        perfil_avanzado=False

    if not user.check_password(request.data['password']):
        return Response({"error": "Invalid"}, status=status.HTTP_404_NOT_FOUND)

    token, _ = Token.objects.get_or_create(user=user)
    serializer = UserSerializers(instance=user)

    return Response({"token": token.key, "user": serializer.data,"perfil_avanzado":perfil_avanzado}, status=status.HTTP_200_OK)




@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated,EsPerfilBasico])
def profile_basico(request):
    return Response({"message": "Acceso básico autorizado"})

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated,EsPerfilAvanzado])
def profile_avanzado(request):
    return Response({"message": "Acceso avanzado autorizado"})
    