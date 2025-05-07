from django.shortcuts import render
from django.db.models import Count
from django.utils import timezone
from django.contrib.admin.views.decorators import staff_member_required
from datetime import timedelta
from .models import Visit
import json

@staff_member_required
def visits_stats(request):
    # Ustalamy okres
    days = int(request.GET.get('days', 30))
    start_date = timezone.now().date() - timedelta(days=days)
    
    # Podstawowe statystyki
    total_visits = Visit.objects.filter(visit_date__gte=start_date).count()
    unique_visitors = Visit.objects.filter(visit_date__gte=start_date).values('ip_address').distinct().count()
    
    # Dzienne wizyty - dla wykresu
    visits_per_day = Visit.objects.filter(visit_date__gte=start_date) \
        .values('visit_date', 'site') \
        .annotate(count=Count('id')) \
        .order_by('visit_date')
    
    # Formatujemy dane dla wykresu
    chart_data = {}
    for site in Visit.objects.values_list('site', flat=True).distinct():
        chart_data[site] = {}
    
    for entry in visits_per_day:
        date_str = entry['visit_date'].strftime('%Y-%m-%d')
        site = entry['site']
        if site not in chart_data:
            chart_data[site] = {}
        chart_data[site][date_str] = entry['count']
    
    # Statystyki per strona
    site_stats = Visit.objects.filter(visit_date__gte=start_date) \
        .values('site') \
        .annotate(count=Count('id')) \
        .order_by('-count')
    
    # Top ścieżki
    path_stats = Visit.objects.filter(visit_date__gte=start_date) \
        .values('path', 'site') \
        .annotate(count=Count('id')) \
        .order_by('-count')[:20]
    
    context = {
        'total_visits': total_visits,
        'unique_visitors': unique_visitors,
        'days': days,
        'site_stats': site_stats,
        'path_stats': path_stats,
        'chart_data': json.dumps(chart_data),
    }
    
    return render(request, 'admin/visits/stats.html', context)