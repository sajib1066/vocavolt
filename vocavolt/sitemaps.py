from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse

from vocablogs.models import Article


class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return [
            'home',
            'customauth:login',
            'customauth:register',
            'customauth:forgot_password',
            'pages:privacy_policy',
            'pages:tos',
            'pages:contact',
            'subscription:pricing',
            'quizzes:quizzes',
            'vocablogs:list',
        ]

    def location(self, item):
        return reverse(item)


class VocablogsSiteMap(Sitemap):
    def items(self):
        return Article.objects.all()
