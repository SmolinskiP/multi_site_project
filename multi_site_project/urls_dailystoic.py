from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import TemplateView
from visits.views import visits_stats
from django.contrib.sitemaps.views import sitemap
from dailystoic.sitemaps import DailyStoicSitemap

handler404 = 'dailystoic.views.custom_404'
handler500 = 'dailystoic.views.custom_500'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('visits-stats/', visits_stats, name='visits_stats'),
    path('', include('dailystoic.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': {'dailystoic': DailyStoicSitemap()}}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', TemplateView.as_view(template_name='dailystoic/robots.txt', content_type='text/plain'), name='robots_txt'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)