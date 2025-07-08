# users/api_views.py

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from django.contrib.auth import authenticate


# @api_view(['POST'])
# def register_user(request):
#     serializer = RegisterSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response({'message': 'Inscription réussie'}, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def register_user(request):
    data = request.data
    user = User.objects.create_user(
        username=data['username'],
        email=data['email'],
        password=data['password'],
        first_name=data.get('first_name', ''),
        last_name=data.get('last_name', '')
    )
    return Response({'message': 'Utilisateur créé'})

class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if user is not None:
            return Response({"message": "Connexion réussie"}, status=status.HTTP_200_OK)
        return Response({"error": "Identifiants invalides"}, status=status.HTTP_401_UNAUTHORIZED)
    
from rest_framework.permissions import IsAuthenticated
from transfers.models import Transfer
from transfers.serializers import TransferSerializer  # ou depuis transfers.serializers si tu le mets ailleurs

class TransferAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        transfers = Transfer.objects.filter(sender=request.user).order_by('-created_at')
        serializer = TransferSerializer(transfers, many=True)
        return Response(serializer.data)