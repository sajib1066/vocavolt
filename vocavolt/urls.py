"""vocavolt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.views.generic.base import TemplateView
from django.conf.urls import handler403, handler404, handler500

from .views import HomePageView, LearningPageView, FlashCardPageView, SectionsPageView, update_word_progress, QuizPageView, submit_quiz_result
from .sitemaps import (
    StaticViewSitemap, VocablogsSiteMap
)

sitemaps = {
    'static': StaticViewSitemap,
    'vocablogs': VocablogsSiteMap,
}

handler403 = 'pages.views.error_403_handler'
handler404 = 'pages.views.error_404_handler'
handler500 = 'pages.views.error_500_handler'


urlpatterns = [
    path('management/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('', HomePageView.as_view(), name='home'),
    path('section/<int:pk>/learn/', LearningPageView.as_view(), name='learn'),
    path('sections/', SectionsPageView.as_view(), name='sections'),
    path('wordpack/<int:pk>/flashcard/', FlashCardPageView.as_view(), name='flashcard'),
    path('wordpack/<int:pk>/quiz/', QuizPageView.as_view(), name='quiz'),
    path('update_word_progress/', update_word_progress, name='update_word_progress'),
    path('submit-quiz-result/', submit_quiz_result, name='submit_quiz_result'),

    path('', include('customauth.urls')),
    path('', include('pages.urls')),
    path('', include('subscription.urls')),
    path('quiz/', include('quizzes.urls')),
    path('dash/', include('dashboard.urls')),
    path('vocablog/', include('vocablogs.urls')),

    # sitemap
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}),

    # robots.txt
    path(
        'robots.txt',
        TemplateView.as_view(
            template_name="pages/robots.txt", content_type="text/plain"
        )
    ),
]

# serve media files in development environment --------------------------------
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
