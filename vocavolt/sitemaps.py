from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse

from flashcards.models import Section


class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return [
            'home',
            'customauth:login',
            'customauth:register',
            'pages:privacy_policy',
            'pages:tos',
            'pages:contact',
            'subscription:pricing',
            'quizzes:quizzes',
        ]

    def location(self, item):
        return reverse(item)


class SectionSiteMap(Sitemap):
    def items(self):
        return Section.objects.all()
