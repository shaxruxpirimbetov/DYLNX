from django.urls import path
from . import views

urlpatterns = [
    path("", views.SubscriptionListCreateAPIView.as_view()),
]