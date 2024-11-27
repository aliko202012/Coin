from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth import authenticate
from apps.user.models import User

from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from apps.user.models import User
from apps.user.serializers import UsersSerializers, UserRegisterSerializer



class UsersApi(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializers
    permission_classes = [IsAuthenticated]


class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)


        if serializer.validated_data['password'] != serializer.validated_data['confirm_password']:
            return Response({'confirm_password': "Пароли не совпадают"}, status=status.HTTP_400_BAD_REQUEST)
        if len(serializer.validated_data['password']) < 8:
            return Response({'password': "Минимум 8 символов"}, status=status.HTTP_400_BAD_REQUEST)


        user = User.objects.create(
            username=serializer.validated_data['username'],
            email=serializer.validated_data['email'],
            phone_number=serializer.validated_data['phone_number'],
            address=serializer.validated_data['address']
        )
        user.set_password(serializer.validated_data['password'])
        user.save()


        response_serializer = self.get_serializer(user)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

class UserLoginAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:

            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key, 
                'balance': user.balance,
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Неверные данные для входа'}, status=status.HTTP_400_BAD_REQUEST)
