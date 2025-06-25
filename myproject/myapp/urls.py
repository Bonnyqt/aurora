from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('pacificstar', views.pacific, name='pacific'),
    path('podium', views.podium, name='podium'),
]