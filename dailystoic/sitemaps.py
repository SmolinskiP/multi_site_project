from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class DailyStoicSitemap(Sitemap):
    priority = 0.7
    changefreq = 'daily'  # Codzienne cytaty = codzienna aktualizacja

    def items(self):
        return ['dailystoic:home', 'dailystoic:newsletter', 'dailystoic:documentation']

    def location(self, item):
        return reverse(item)