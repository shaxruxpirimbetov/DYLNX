from django.views import View
from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, parsers
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserSerializer, UpdateUserSerializer, ResponseUserSerializer
from .permissions import IsMe
User = get_user_model()

class UserListCreateAPIView(generics.ListCreateAPIView):
    parser_classes = [parsers.JSONParser, parsers.MultiPartParser, parsers.FormParser]
    queryset = User.objects.all()
    permission_classes = [permissions.IsAdminUser]

    def get_serializer_class(self):
        if self.request.user.is_authenticated and self.request.user.is_superuser:
            return UserSerializer
        return ResponseUserSerializer

class UserDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    parser_classes = [parsers.JSONParser, parsers.MultiPartParser, parsers.FormParser]
    queryset = User.objects.all()
    permission_classes = [IsMe]

    def get_serializer_class(self):
        if self.request.user.is_authenticated and self.request.user.is_superuser and self.request.method == "GET":
            return UserSerializer
        elif self.request.method == "GET":
            return ResponseUserSerializer
        return UpdateUserSerializer

class MeAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        if self.request.user.is_authenticated and self.request.user.is_superuser:
            return Response(UserSerializer(request.user).data, status=200)
        return Response(ResponseUserSerializer(request.user).data, status=200)

class TeamAPIView(generics.ListAPIView):
    serializer_class = ResponseUserSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return User.objects.filter(role="EMPLOYEE")

class IndexView(APIView):
    def get(self, request):
        return render(request, 'index.html')