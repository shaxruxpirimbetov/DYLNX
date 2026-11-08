from rest_framework import generics, permissions, parsers
from rest_framework.response import Response

from .models import Project, ProjectImage
from .serializers import ProjectSerializer

class ProjectListCreateAPIView(generics.ListCreateAPIView):
    parser_classes = [parsers.JSONParser, parsers.MultiPartParser, parsers.FileUploadParser]
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        images = request.FILES.getlist('images')
        for i in images:
            ProjectImage.objects.create(project=serializer.instance, image=i)
        return Response(ProjectSerializer(serializer.instance).data, status=201)

class ProjectDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    parser_classes = [parsers.JSONParser, parsers.MultiPartParser, parsers.FileUploadParser]
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]