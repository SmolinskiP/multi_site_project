from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import TemplateView
from visits.views import visits_stats

handler404 = 'dailystoic.views.custom_404'
handler500 = 'dailystoic.views.custom_500'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('visits-stats/', visits_stats, name='visits_stats'),
    path('', include('dailystoic.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)