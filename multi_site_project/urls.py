from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.conf import settings
from django.conf.urls.static import static
from ashes.views import custom_404, custom_500

urlpatterns = [
    path('admin/', admin.site.urls),
]
handler404 = 'ashes.views.custom_404'  # Pełna ścieżka do modułu
handler500 = 'ashes.views.custom_500'