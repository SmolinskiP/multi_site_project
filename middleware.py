class DomainMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.get_host().split(':')[0]

        # Przekierowanie żądań na podstawie domeny
        if 'ashes.pl' in host:
            request.path_info = '/ashes' + request.path_info
        elif 'dailystoic.pl' in host:
            request.path_info = '/dailystoic' + request.path_info

        return self.get_response(request)
