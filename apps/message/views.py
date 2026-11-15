from rest_framework import generics, permissions
from .models import Message
from .serializers import MessageSerializer

class MessageListCreateAPIView(generics.ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def get_permissions(self):
        return [permissions.AllowAny()] if self.request.method == "POST" else [permissions.IsAdminUser()]