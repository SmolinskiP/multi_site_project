from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.urls import reverse
from .models import Quote, NewsletterSubscriber
from .forms import NewsletterSubscriptionForm, TestEmailForm
from django.utils import timezone
import datetime
import base64
from .utils import send_dailystoic_email
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_GET

# Słownik do tłumaczenia nazw miesięcy na język polski
POLISH_MONTHS = {
    1: 'stycznia',
    2: 'lutego',
    3: 'marca',
    4: 'kwietnia',
    5: 'maja',
    6: 'czerwca',
    7: 'lipca',
    8: 'sierpnia',
    9: 'września',
    10: 'października',
    11: 'listopada',
    12: 'grudnia'
}

MAIL_TITLES = {
    1: "Styczeń: Jasność",
    2: "Luty: Namiętności i emocje",
    3: "Marzec: Świadomość",
    4: "Kwiecień: Obiektywna myśl",
    5: "Maj: Właściwe działania",
    6: "Czerwiec: Rozwiązywanie problemów",
    7: "Lipiec: Powinności",
    8: "Sierpień: Pragmatyzm",
    9: "Wrzesień: Hart ducha i odporność",
    10: "Październik: Cnota i dobroć",
    11: "Listopad: Akceptacja - amor fati",
    12: "Grudzień: Rozmyślania nad śmiertelnością"
}

def home(request):
    """Widok strony głównej z dzisiejszym cytatem"""
    daily_quote = Quote.get_todays_quote()
    
    # Uzyskujemy aktualną datę
    today = timezone.now().date()
    polish_date = f"{today.day} {POLISH_MONTHS[today.month]} {today.year}"
    
    context = {
        'daily_quote': daily_quote,
        'polish_date': polish_date
    }
    return render(request, 'dailystoic/home.html', context)

def newsletter_placeholder(request):
    """Tymczasowy placeholder dla strony newslettera"""
    return HttpResponse('<h1>Strona newslettera jest w trakcie budowy</h1><p><a href="/">Wróć na stronę główną</a></p>')

def documentation(request):
    """Widok strony dokumentacji"""
    return render(request, 'dailystoic/documentation.html')

def newsletter(request):
    """Widok strony newslettera z formularzem zapisu"""
    form = NewsletterSubscriptionForm()
    return render(request, 'dailystoic/newsletter.html', {'form': form})

def newsletter_subscribe(request):
    """Obsługa formularza zapisu do newslettera"""
    if request.method == 'POST':
        form = NewsletterSubscriptionForm(request.POST)
        
        # Sprawdź, czy adres email już istnieje w bazie
        email = form.data.get('email')
        existing_subscriber = None
        
        if email:
            try:
                existing_subscriber = NewsletterSubscriber.objects.get(email=email)
            except NewsletterSubscriber.DoesNotExist:
                pass
        
        # Jeśli subskrybent istnieje, ale jest nieaktywny - reaktywuj go
        if existing_subscriber and not existing_subscriber.is_active:
            existing_subscriber.is_active = True
            existing_subscriber.save()
            
            # Wysyłamy email potwierdzający reaktywację
            send_welcome_email(existing_subscriber.email)
            
            messages.success(request, "Twoja subskrypcja została ponownie aktywowana! Jeśli nie otrzymałeś powitalnej wiadomości, sprawdź folder ze spamem.")
            return redirect('dailystoic:newsletter')
        
        # Jeśli subskrybent istnieje i jest aktywny - poinformuj użytkownika
        elif existing_subscriber and existing_subscriber.is_active:
            messages.info(request, "Ten adres email jest już zapisany do newslettera.")
            return redirect('dailystoic:newsletter')
        
        # W przeciwnym wypadku - standardowa walidacja i zapis nowego subskrybenta
        elif form.is_valid():
            subscriber = form.save()
            
            # Wysyłamy email potwierdzający
            send_welcome_email(subscriber.email)
            
            messages.success(request, "Dziękujemy za zapisanie się do newslettera! Jeśli nie otrzymałeś powitalnej wiadomości, sprawdź folder ze spamem.")
            return redirect('dailystoic:newsletter')
    else:
        form = NewsletterSubscriptionForm()
    
    return render(request, 'dailystoic/newsletter.html', {'form': form})

def newsletter_unsubscribe(request, email):
    """Obsługa anulowania subskrypcji"""
    try:
        subscriber = NewsletterSubscriber.objects.get(email=email)
        subscriber.is_active = False
        subscriber.save()
        return render(request, 'dailystoic/unsubscribe.html', {'email': email})
    except NewsletterSubscriber.DoesNotExist:
        return render(request, 'dailystoic/unsubscribe.html', {'error': True})

def send_welcome_email(email):
    """Wysyła powitalny email po zapisaniu się do newslettera"""
    current_month = timezone.now().month
    mail_title = MAIL_TITLES.get(current_month, "DailyStoic")

    subject = f"[DailyStoic] {mail_title} - Witaj w społeczności stoików"
    
    # Pobierz dzisiejszy cytat (lub przykładowy, jeśli nie ma)
    daily_quote = Quote.get_todays_quote()
    
    if not daily_quote:
        daily_quote = {
            'title': 'Witaj w społeczności stoików',
            'content': '"Nie mów mało, ale niekoniecznie dużo. I nie mów bezużytecznych słów." — Marek Aureliusz, Rozmyślania',
            'reflection': 'Dziękujemy za dołączenie do naszej społeczności. Od jutra będziesz otrzymywać codzienną dawkę stoickiej mądrości.'
        }
    
    # Pobierz miesiąc do obrazka
    current_month = timezone.now().month
    month_names = {
        1: 'sty', 2: 'lut', 3: 'mar', 4: 'kwi', 5: 'maj', 6: 'cze',
        7: 'lip', 8: 'sie', 9: 'wrz', 10: 'paz', 11: 'lis', 12: 'gru'
    }
    img_name = f"{month_names[current_month]}.jpg"
    
    # Kontekst do szablonu emaila
    context = {
        'title': daily_quote.title if hasattr(daily_quote, 'title') else daily_quote['title'],
        'quote': daily_quote.content if hasattr(daily_quote, 'content') else daily_quote['content'],
        'reflection': daily_quote.reflection if hasattr(daily_quote, 'reflection') else daily_quote['reflection'],
        'img_name': img_name,
        'unsubscribe_url': f"{settings.SITE_URL}{reverse('dailystoic:newsletter_unsubscribe', args=[email])}"
    }
    
    # Renderuj HTML
    html_content = render_to_string('dailystoic/email/welcome_email.html', context)
    
    # Wysyłaj email używając konfiguracji DailyStoic
    send_dailystoic_email(subject, html_content, [email])

@staff_member_required
def test_newsletter(request):
    """Strona testowa do wysyłania maili (tylko dla administratorów)"""
    sent = False
    error = None
    
    if request.method == 'POST':
        form = TestEmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            
            # Pobierz dzisiejszy cytat
            daily_quote = Quote.get_todays_quote()
            
            if not daily_quote:
                error = "Brak cytatu na dzisiaj!"
            else:
                # Pobierz miesiąc do obrazka
                current_month = timezone.now().month
                month_names = {
                    1: 'sty', 2: 'lut', 3: 'mar', 4: 'kwi', 5: 'maj', 6: 'cze',
                    7: 'lip', 8: 'sie', 9: 'wrz', 10: 'paz', 11: 'lis', 12: 'gru'
                }
                img_name = f"{month_names[current_month]}.jpg"
                
                # Przygotuj email
                subject = f"[DailyStoic TEST] {daily_quote.title}"
                
                # Kontekst emaila
                context = {
                    'title': daily_quote.title,
                    'quote': daily_quote.content,
                    'reflection': daily_quote.reflection,
                    'img_name': img_name,
                    'unsubscribe_url': f"{settings.SITE_URL}{reverse('dailystoic:newsletter_unsubscribe', args=[email])}"
                }
                
                # Renderuj HTML
                html_content = render_to_string('dailystoic/email/daily_quote_email.html', context)
                
                # Wysyłaj email
                from .utils import send_dailystoic_email
                if send_dailystoic_email(subject, html_content, [email]):
                    sent = True
                else:
                    error = "Wystąpił błąd podczas wysyłania emaila."
    else:
        form = TestEmailForm()
    
    return render(request, 'dailystoic/test_newsletter.html', {
        'form': form,
        'sent': sent,
        'error': error
    })

def custom_404(request, exception):
    return render(request, 'dailystoic/404.html', status=404)

def custom_500(request):
    return render(request, 'dailystoic/500.html', status=500)

def test_404(request):
    """
    Widok testowy do sprawdzenia strony 404
    """
    # Wysyła HttpResponseNotFound
    from django.http import Http404
    raise Http404("Test strony 404")

def test_500(request):
    """
    Widok testowy do sprawdzenia strony 500
    """
    # Celowo wywołuje wyjątek, aby wywołać błąd 500
    raise Exception("Test strony 500")

@require_GET
def robots_txt(request):
    content = render_to_string('dailystoic/robots.txt', {'domain': request.get_host()})
    return HttpResponse(content, content_type='text/plain')

def about_me(request):
    return render(request, 'dailystoic/about_me.html')