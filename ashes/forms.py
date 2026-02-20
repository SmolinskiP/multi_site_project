# forms.py
from django import forms
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox
from .models import ContactMessage

class ContactForm(forms.ModelForm):
    captcha = ReCaptchaField(
        widget=ReCaptchaV2Checkbox(
            attrs={
                'data-theme': 'dark',
            }
        ),
        label=''
    )

    privacy = forms.BooleanField(
        required=True,
        label="Wyrażam zgodę na przetwarzanie moich danych osobowych zgodnie z polityką prywatności."
    )

    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Twoje imię i nazwisko'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Twój adres email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Opcjonalnie'}),
            'subject': forms.Select(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control form-textarea', 'rows': 5, 'placeholder': 'Treść wiadomości'})
        }