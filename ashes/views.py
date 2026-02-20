# views.py - Zmodyfikowany widok z obsługą bazy danych
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from .models import Category, GalleryImage, ContactMessage
from .forms import ContactForm
import logging

logger = logging.getLogger(__name__)

def home(request):
    return render(request, 'ashes/home.html')

def gallery_view(request):
    # Pobieramy kategorie z bazy danych
    categories = Category.objects.all()
    
    # Pobieramy wszystkie obrazy z bazy danych
    images = GalleryImage.objects.all().select_related('category')
    
    context = {
        'categories': categories,
        'images': images
    }
    
    return render(request, 'ashes/gallery.html', context)

def workshops_view(request):
    return render(request, 'ashes/workshops.html')

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Zapisz wiadomość do bazy danych
            message = ContactMessage(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                phone=form.cleaned_data['phone'],
                subject=form.cleaned_data['subject'],
                message=form.cleaned_data['message']
            )
            message.save()
            
            # Spróbuj wysłać email z powiadomieniem
            try:
                email_subject = f'Nowa wiadomość: {form.cleaned_data["subject"]}'
                email_message = f'Otrzymałeś nową wiadomość od {form.cleaned_data["name"]} ({form.cleaned_data["email"]}):\n\n{form.cleaned_data["message"]}'
                
                # Logowanie przed próbą wysłania
                logger.info(f"Próba wysłania emaila na adres: {settings.CONTACT_EMAIL}")
                logger.info(f"Z adresu: {settings.DEFAULT_FROM_EMAIL}")
                logger.info(f"Temat: {email_subject}")
                
                result = send_mail(
                    email_subject,
                    email_message,
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.CONTACT_EMAIL],
                    fail_silently=False,
                )
                
                # Logowanie po próbie wysłania
                logger.info(f"Wynik wysyłania emaila: {result}")
                
                messages.success(request, 'Twoja wiadomość została wysłana. Dziękujemy za kontakt!')
            except Exception as e:
                # Logowanie wyjątku
                logger.error(f"Błąd podczas wysyłania emaila: {str(e)}")
                
                # Wiadomość zapisana w bazie danych, ale email nie został wysłany
                messages.warning(request, 'Twoja wiadomość została zapisana, ale wystąpił problem z wysłaniem emaila. Skontaktujemy się z Tobą wkrótce!')
                
            return redirect('ashes:contact')
        else:
            # Jeśli formularz zawiera błędy, wyświetl je
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Błąd w polu {field}: {error}")
            
    else:
        form = ContactForm()
    
    return render(request, 'ashes/contact.html', {'form': form})

def custom_404(request, exception):
    return render(request, 'ashes/404.html', status=404)

def custom_500(request):
    return render(request, 'ashes/500.html', status=500)

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

def about_me(request):
    return render(request, 'ashes/about_me.html')