from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class StaticViewSitemap(Sitemap):
    def items(self):
        return [
            {'url': 'ashes:home', 'priority': 1.0, 'changefreq': 'weekly'},
            {'url': 'ashes:gallery', 'priority': 0.8, 'changefreq': 'weekly'},
            {'url': 'ashes:workshops', 'priority': 0.7, 'changefreq': 'monthly'},
            {'url': 'ashes:about_me', 'priority': 0.9, 'changefreq': 'yearly'},
            {'url': 'ashes:contact', 'priority': 0.6, 'changefreq': 'monthly'},
        ]

    def location(self, item):
        return reverse(item['url'])

    def priority(self, item):
        return item['priority']

    def changefreq(self, item):
        return item['changefreq']