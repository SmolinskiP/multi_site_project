# visits/middleware.py
from django.utils import timezone
from ipware import get_client_ip
from .models import Visit

class VisitTrackerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Wyciągamy dane przed przetworzeniem requestu
        response = self.get_response(request)
        
        # Nie śledzimy adminów i botów
        if not self._should_track(request):
            return response
            
        # Pobieramy IP klienta
        ip, is_routable = get_client_ip(request)
        if not ip:
            return response
            
        # Identyfikujemy stronę na podstawie current_site
        site = getattr(request, 'current_site', 'default')
        
        # Zapisujemy wizytę
        today = timezone.now().date()
        Visit.objects.get_or_create(
            ip_address=ip,
            visit_date=today,
            site=site,
            defaults={
                'user_agent': request.META.get('HTTP_USER_AGENT', ''),
                'path': request.path[:255],
                'referer': request.META.get('HTTP_REFERER', '')
            }
        )
        
        return response
        
    def _should_track(self, request):
        # Nie śledzimy adminów
        if request.path.startswith('/admin/'):
            return False
            
        # Sprawdzamy czy to nie jest bot
        user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
        bot_indicators = ['bot', 'crawler', 'spider', 'slurp', 'bingbot', 'googlebot']
        if any(bot in user_agent for bot in bot_indicators):
            return False
            
        return True