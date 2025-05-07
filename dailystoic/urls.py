from django.urls import path
from django.views.static import serve
from django.conf import settings
import os
from . import views

app_name = 'dailystoic'

urlpatterns = [
    path('', views.home, name='home'),
    path('newsletter/', views.newsletter, name='newsletter'),
    path('newsletter/subscribe/', views.newsletter_subscribe, name='newsletter_subscribe'),
    path('newsletter/unsubscribe/<str:email>/', views.newsletter_unsubscribe, name='newsletter_unsubscribe'),
    path('newsletter/test/', views.test_newsletter, name='test_newsletter'),
    path('documentation/', views.documentation, name='documentation'),
    path('test_404/', views.test_404, name='test_404'),
    path('test_500/', views.test_500, name='test_500'),

    path('quote/text_pl.json', serve, {
        'document_root': os.path.join(settings.MEDIA_ROOT, 'dailystoic/quote'),
        'path': 'text_pl.json',
    }),
    path('quote/text_en.json', serve, {
        'document_root': os.path.join(settings.MEDIA_ROOT, 'dailystoic/quote'),
        'path': 'text_en.json',
    }),
    path('daily.png', serve, {
        'document_root': os.path.join(settings.MEDIA_ROOT, 'dailystoic'),
        'path': 'daily.png',
    }),
    path('daily_en.png', serve, {
        'document_root': os.path.join(settings.MEDIA_ROOT, 'dailystoic'),
        'path': 'daily_en.png',
    }),
    path('empty.png', serve, {
        'document_root': os.path.join(settings.MEDIA_ROOT, 'dailystoic'),
        'path': 'empty.png',
    }),
    path('empty_en.png', serve, {
        'document_root': os.path.join(settings.MEDIA_ROOT, 'dailystoic'),
        'path': 'empty_en.png',
    }),
]