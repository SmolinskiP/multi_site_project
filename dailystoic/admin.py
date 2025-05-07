from django.contrib import admin
from .models import Quote, NewsletterSubscriber

class QuoteAdmin(admin.ModelAdmin):
    list_display = ('date_display', 'title', 'content_preview', 'is_published')
    list_filter = ('is_published', 'date')
    search_fields = ('title', 'content', 'reflection')
    list_editable = ('is_published',)
    date_hierarchy = 'date'
    list_per_page = 20
    
    def content_preview(self, obj):
        """Skrócona treść cytatu dla listy w adminie"""
        return obj.content[:80] + '...' if len(obj.content) > 80 else obj.content
    content_preview.short_description = 'Treść cytatu'
    
    def date_display(self, obj):
        """Wyświetlanie daty w formacie DD MMMM"""
        return obj.date.strftime('%d %B')
    date_display.short_description = 'Data'
    date_display.admin_order_field = 'date'
    
    fieldsets = (
        ('Podstawowe informacje', {
            'fields': ('date', 'title', 'is_published')
        }),
        ('Treść', {
            'fields': ('content', 'reflection'),
            'classes': ('wide',)
        }),
    )

admin.site.register(Quote, QuoteAdmin)

@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_active', 'date_added')
    list_filter = ('is_active',)
    search_fields = ('email',)
    date_hierarchy = 'date_added'
    ordering = ('-date_added',)
    actions = ['make_active', 'make_inactive', 'send_test_email']
    
    def make_active(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'Aktywowano {updated} subskrypcji.')
    make_active.short_description = "Aktywuj wybrane subskrypcje"
    
    def make_inactive(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'Dezaktywowano {updated} subskrypcji.')
    make_inactive.short_description = "Dezaktywuj wybrane subskrypcje"
    
    def send_test_email(self, request, queryset):
        from .utils import send_dailystoic_email
        from django.template.loader import render_to_string
        from django.utils import timezone
        from .models import Quote
        from django.urls import reverse
        from django.conf import settings
        
        daily_quote = Quote.get_todays_quote()
        if not daily_quote:
            self.message_user(request, f'Błąd: Brak cytatu na dzisiaj!', level='error')
            return
        
        # Pobierz miesiąc do obrazka
        current_month = timezone.now().month
        month_names = {
            1: 'sty', 2: 'lut', 3: 'mar', 4: 'kwi', 5: 'maj', 6: 'cze',
            7: 'lip', 8: 'sie', 9: 'wrz', 10: 'paz', 11: 'lis', 12: 'gru'
        }
        img_name = f"{month_names[current_month]}.jpg"
        
        # Przygotuj email
        subject = f"[DailyStoic TEST] {daily_quote.title}"
        
        sent_count = 0
        error_count = 0
        
        for subscriber in queryset:
            # Kontekst emaila
            context = {
                'title': daily_quote.title,
                'quote': daily_quote.content,
                'reflection': daily_quote.reflection,
                'img_name': img_name,
                'unsubscribe_url': f"{settings.SITE_URL}{reverse('dailystoic:newsletter_unsubscribe', args=[subscriber.email])}"
            }
            
            # Renderuj HTML
            html_content = render_to_string('dailystoic/email/daily_quote_email.html', context)
            
            # Wysyłaj email
            if send_dailystoic_email(subject, html_content, [subscriber.email]):
                sent_count += 1
            else:
                error_count += 1
        
        if error_count:
            self.message_user(request, f'Wysłano testowy email do {sent_count} subskrybentów. Błędy: {error_count}', level='warning')
        else:
            self.message_user(request, f'Wysłano testowy email do {sent_count} subskrybentów.', level='success')
    
    send_test_email.short_description = "Wyślij testowy email do wybranych subskrybentów"