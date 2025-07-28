from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('pacificstar', views.pacific, name='pacific'),
    path('podium', views.podium, name='podium'),
    path('pacific2', views.pacific2, name='pacific2'),
    path('podium2', views.podium2, name='podium2'),
    path('about', views.about, name='about'),
    path('reserve', views.reserve, name='reserve'),
    path('reservation', views.reservation_view, name='reservation_view'),  # Add this line
    path('newsletter-subscribe', views.newsletter_subscribe, name='newsletter_subscribe'),
    path('contact', views.contact, name='contact'),
    path('view-menu', views.view_menu, name='view_menu'),
]