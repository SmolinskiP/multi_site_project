from django import forms
from .models import NewsletterSubscriber

class NewsletterSubscriptionForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscriber
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'newsletter-input', 'placeholder': 'Twój adres email'})
        }
    
    def clean_email(self):
        email = self.cleaned_data['email']
        return email
    
class TestEmailForm(forms.Form):
    email = forms.EmailField(
        label="Adres email do testu",
        widget=forms.EmailInput(attrs={'class': 'newsletter-input', 'placeholder': 'Twój adres email'})
    )
