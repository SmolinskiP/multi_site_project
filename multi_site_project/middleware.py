class DomainMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Wykrywanie domeny
        host = request.get_host().split(':')[0]
        
        # Dodanie informacji o domenie do requesta
        if 'ashes.pl' in host:
            request.current_site = 'ashes'
            request.urlconf = 'multi_site_project.urls_ashes'
        elif 'dailystoic.pl' in host:
            request.current_site = 'dailystoic'
            request.urlconf = 'multi_site_project.urls_dailystoic'
        else:
            request.current_site = 'default'
            
        return self.get_response(request)