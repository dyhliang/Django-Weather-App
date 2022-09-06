from django.urls import path
from . import views

urlpatterns = [
    path('', views.index)  # Path for our index view page
]