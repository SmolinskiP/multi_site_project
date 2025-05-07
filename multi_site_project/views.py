from django.shortcuts import render

def maintenance_page(request):
    # Rozpoznanie domeny
    host = request.get_host().split(':')[0]
    
    context = {
        'domain': host
    }
    
    return render(request, 'maintenance.html', context)