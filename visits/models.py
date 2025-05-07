# visits/models.py
from django.db import models
from django.utils import timezone

class Visit(models.Model):
    ip_address = models.GenericIPAddressField()
    visit_date = models.DateField(default=timezone.now)
    site = models.CharField(max_length=100)
    user_agent = models.TextField(blank=True, null=True)
    path = models.CharField(max_length=255)
    referer = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('ip_address', 'visit_date', 'site')
        indexes = [
            models.Index(fields=['site', 'visit_date']),
        ]
        
    def __str__(self):
        return f"{self.ip_address} - {self.site} - {self.visit_date}"