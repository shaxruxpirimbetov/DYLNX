from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.db import models

class Project(models.Model):
    title = models.CharField(max_length=100, validators=[MinLengthValidator(3), MaxLengthValidator(100)])
    description = models.TextField(
        validators=[MinLengthValidator(3), MaxLengthValidator(1000)]
    )
    logo = models.ImageField(upload_to='projects/logos/')
    link = models.URLField(max_length=500, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Project {self.title}"

    class Meta:
        verbose_name_plural = "Projects"
        ordering = ['-created_at']

class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="project_image_project")
    image = models.ImageField(upload_to='projects/images/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Project {self.project.title}"

    class Meta:
        verbose_name_plural = "Project Images"
        ordering = ['-created_at']