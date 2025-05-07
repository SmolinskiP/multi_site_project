from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from ashes.sitemaps import StaticViewSitemap
from django.views.generic.base import TemplateView
from ashes.views import custom_404, custom_500
from visits.views import visits_stats

handler404 = 'ashes.views.custom_404'  # Pełna ścieżka do modułu
handler500 = 'ashes.views.custom_500'

sitemaps = {
    'static': StaticViewSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('visits-stats/', visits_stats, name='visits_stats'),
    path('', include('ashes.urls')),
    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)