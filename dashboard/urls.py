from django.urls import path

from dashboard.views import WordCreateView

app_name = "dashboard"


urlpatterns = [
    path('words/create/', WordCreateView.as_view(), name='word_create'),
]
