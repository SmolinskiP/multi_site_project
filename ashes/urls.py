# urls.py - tylko ścieżki URL
from django.urls import path
from . import views

app_name = 'ashes'

urlpatterns = [
    path('', views.home, name='home'),
    path('gallery/', views.gallery_view, name='gallery'),
    path('galeria/', views.gallery_view, name='galeria'),
    path('workshops/', views.workshops_view, name='workshops'),
    path('warsztaty/', views.workshops_view, name='warsztaty'),
    path('contact/', views.contact_view, name='contact'),
    path('kontakt/', views.contact_view, name='kontakt'),
    path('o-mnie/', views.about_me, name='about_me'),
    path('test_404/', views.test_404, name='test_404'),
    path('test_500/', views.test_500, name='test_500'),
]