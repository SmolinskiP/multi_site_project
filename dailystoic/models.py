from django.db import models
from django.utils import timezone
import datetime

class Quote(models.Model):
    date = models.DateField(verbose_name="Data", unique=True)
    title = models.CharField(max_length=200, verbose_name="Tytuł")
    content = models.TextField(verbose_name="Treść cytatu") # Razem z autorem i źródłem
    reflection = models.TextField(verbose_name="Refleksja")
    is_published = models.BooleanField(default=True, verbose_name="Opublikowany")
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.date.strftime('%d.%m')} - {self.title}"
    
    class Meta:
        verbose_name = "Cytat"
        verbose_name_plural = "Cytaty"
        ordering = ['date']
    
    @classmethod
    def get_todays_quote(cls):
        """Zwraca cytat na dzisiejszy dzień."""
        today = timezone.now().date()
        # Pobieramy dzień i miesiąc z dzisiejszej daty
        month = today.month
        day = today.day
        
        # Szukamy cytatu na ten dzień i miesiąc (rok nie ma znaczenia)
        try:
            return cls.objects.get(date__month=month, date__day=day, is_published=True)
        except cls.DoesNotExist:
            return None
        except cls.MultipleObjectsReturned:
            # W przypadku wielu cytatów na ten sam dzień, wybieramy najnowszy
            return cls.objects.filter(date__month=month, date__day=day, is_published=True).order_by('-date').first()
    
    def get_next_quote(self):
        """Zwraca następny cytat w kolejności dat."""
        # Pobieramy miesiąc i dzień z daty bieżącego cytatu
        current_month = self.date.month
        current_day = self.date.day
        
        # Najpierw szukamy cytatu z tym samym miesiącem, ale większym dniem
        next_quote = Quote.objects.filter(
            date__month=current_month, 
            date__day__gt=current_day,
            is_published=True
        ).order_by('date__day').first()
        
        if next_quote:
            return next_quote
        
        # Jeśli nie znaleziono, szukamy pierwszego cytatu w następnym miesiącu
        next_month = current_month + 1 if current_month < 12 else 1
        
        next_quote = Quote.objects.filter(
            date__month=next_month,
            is_published=True
        ).order_by('date__day').first()
        
        if next_quote:
            return next_quote
        
        # Jeśli nadal nie znaleziono, wracamy do pierwszego cytatu w roku
        return Quote.objects.filter(is_published=True).order_by('date__month', 'date__day').first()
    
    def get_prev_quote(self):
        """Zwraca poprzedni cytat w kolejności dat."""
        # Pobieramy miesiąc i dzień z daty bieżącego cytatu
        current_month = self.date.month
        current_day = self.date.day
        
        # Najpierw szukamy cytatu z tym samym miesiącem, ale mniejszym dniem
        prev_quote = Quote.objects.filter(
            date__month=current_month, 
            date__day__lt=current_day,
            is_published=True
        ).order_by('-date__day').first()
        
        if prev_quote:
            return prev_quote
        
        # Jeśli nie znaleziono, szukamy ostatniego cytatu w poprzednim miesiącu
        prev_month = current_month - 1 if current_month > 1 else 12
        
        prev_quote = Quote.objects.filter(
            date__month=prev_month,
            is_published=True
        ).order_by('-date__day').first()
        
        if prev_quote:
            return prev_quote
        
        # Jeśli nadal nie znaleziono, wracamy do ostatniego cytatu w roku
        return Quote.objects.filter(is_published=True).order_by('-date__month', '-date__day').first()
    
class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True, verbose_name="Adres email")
    is_active = models.BooleanField(default=True, verbose_name="Aktywny")
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name = "Subskrybent newslettera"
        verbose_name_plural = "Subskrybenci newslettera"