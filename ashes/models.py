# models.py - zaktualizowane modele
from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit
from pilkit.processors import Transpose

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

class GalleryImage(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='gallery/')
    thumbnail = ImageSpecField(source='image',
                                processors=[Transpose(), ResizeToFit(600, 600)],
                                format='JPEG',
                                options={'quality': 85})
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='images')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']

class ContactMessage(models.Model):
    SUBJECT_CHOICES = (
        ('pokaz', 'Zapytanie o pokaz'),
        ('warsztaty', 'Zapytanie o warsztaty'),
        ('współpraca', 'Propozycja współpracy'),
        ('inne', 'Inne'),
    )
    
    name = models.CharField(max_length=100, verbose_name="Imię i nazwisko")
    email = models.EmailField(verbose_name="Adres email")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Numer telefonu")
    subject = models.CharField(max_length=20, choices=SUBJECT_CHOICES, verbose_name="Temat")
    message = models.TextField(verbose_name="Wiadomość")
    is_read = models.BooleanField(default=False, verbose_name="Przeczytane")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data utworzenia")
    
    def __str__(self):
        return f"{self.name} - {self.get_subject_display()} ({self.created_at.strftime('%d-%m-%Y')})"
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Wiadomość kontaktowa"
        verbose_name_plural = "Wiadomości kontaktowe"