from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class DailyStoicSitemap(Sitemap):
    def items(self):
        return [
            {'url': 'dailystoic:home', 'priority': 1.0, 'changefreq': 'daily'},  # Główna strona z codziennymi cytatami
            {'url': 'dailystoic:newsletter', 'priority': 0.8, 'changefreq': 'weekly'},
            {'url': 'dailystoic:about_me', 'priority': 0.9, 'changefreq': 'yearly'},
            {'url': 'dailystoic:documentation', 'priority': 0.4, 'changefreq': 'monthly'},
        ]

    def location(self, item):
        return reverse(item['url'])

    def priority(self, item):
        return item['priority']

    def changefreq(self, item):
        return item['changefreq']