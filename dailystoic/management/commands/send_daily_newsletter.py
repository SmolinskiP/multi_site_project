# dailystoic/management/commands/send_daily_newsletter.py
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django.conf import settings
from dailystoic.models import Quote, NewsletterSubscriber
from dailystoic.utils import send_dailystoic_email, get_unsubscribe_url
from django.utils import timezone
import time

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

class Command(BaseCommand):
    help = 'Wysyła dzisiejszy cytat do wszystkich aktywnych subskrybentów newslettera'
    
    def handle(self, *args, **options):
        # Pobierz dzisiejszy cytat
        daily_quote = Quote.get_todays_quote()
        
        if not daily_quote:
            self.stdout.write(self.style.ERROR('Brak cytatu na dzisiaj!'))
            return
        
        # Pobierz wszystkich aktywnych subskrybentów
        subscribers = NewsletterSubscriber.objects.filter(is_active=True)
        
        if not subscribers:
            self.stdout.write(self.style.WARNING('Brak aktywnych subskrybentów.'))
            return
        
        # Pobierz miesiąc do obrazka
        current_month = timezone.now().month
        mail_title = MAIL_TITLES.get(current_month, "DailyStoic")

        month_names = {
            1: 'sty', 2: 'lut', 3: 'mar', 4: 'kwi', 5: 'maj', 6: 'cze',
            7: 'lip', 8: 'sie', 9: 'wrz', 10: 'paz', 11: 'lis', 12: 'gru'
        }
        img_name = f"{month_names[current_month]}.jpg"
        
        # Przygotuj email
        subject = f"[DailyStoic] {mail_title} - {daily_quote.title}"
        
        # Kontekst podstawowy dla szablonu
        base_context = {
            'title': daily_quote.title,
            'quote': daily_quote.content,
            'reflection': daily_quote.reflection,
            'img_name': img_name,
        }
        
        sent_count = 0
        errors_count = 0
        
        # Wysyłaj do każdego subskrybenta
        for subscriber in subscribers:
            # Dodaj unsubscribe URL specyficzny dla tego subskrybenta
            context = base_context.copy()
            context['unsubscribe_url'] = get_unsubscribe_url(subscriber.email)
            
            # Renderuj zawartość
            html_content = render_to_string('dailystoic/email/daily_quote_email.html', context)
            
            # Twórz i wysyłaj wiadomość
            try:
                if send_dailystoic_email(subject, html_content, [subscriber.email]):
                    sent_count += 1
                    self.stdout.write(f"Wysłano email do: {subscriber.email}")
                else:
                    errors_count += 1
                    self.stdout.write(self.style.ERROR(f"Błąd wysyłania do {subscriber.email}"))
                # Małe opóźnienie między mailami
                time.sleep(5)
            except Exception as e:
                errors_count += 1
                self.stdout.write(self.style.ERROR(f"Błąd wysyłania do {subscriber.email}: {e}"))
        
        self.stdout.write(self.style.SUCCESS(f"Wysłano newsletter do {sent_count} subskrybentów (błędy: {errors_count})."))