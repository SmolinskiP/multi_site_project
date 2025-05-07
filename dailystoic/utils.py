# dailystoic/utils.py
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def get_unsubscribe_url(email):
    """
    Generuje absolutny URL do anulowania subskrypcji bez użycia reverse()
    """
    # Ponieważ mamy wiele domen, budujemy URL bezpośrednio
    return f"https://dailystoic.pl/newsletter/unsubscribe/{email}/"

def send_dailystoic_email(subject, html_content, recipient_list, from_email=None):
    """
    Wysyła email używając konfiguracji DailyStoic
    """
    if from_email is None:
        from_email = settings.DAILYSTOIC_FROM_EMAIL
    
    # Tworzenie wiadomości
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = from_email
    
    # Dodaj treść HTML
    part = MIMEText(html_content, 'html', 'utf-8')
    msg.attach(part)
    
    # Konfiguracja SMTP
    try:
        server = smtplib.SMTP(settings.DAILYSTOIC_EMAIL_HOST, settings.DAILYSTOIC_EMAIL_PORT)
        server.ehlo()
        
        if settings.DAILYSTOIC_EMAIL_USE_TLS:
            server.starttls()
            server.ehlo()
        
        server.login(settings.DAILYSTOIC_EMAIL_HOST_USER, settings.DAILYSTOIC_EMAIL_HOST_PASSWORD)
        
        # Wysyłanie do wszystkich odbiorców
        for recipient in recipient_list:
            msg['To'] = recipient
            server.sendmail(from_email, recipient, msg.as_string())
        
        server.quit()
        return True
    except Exception as e:
        print(f"Błąd wysyłki maila: {e}")
        return False