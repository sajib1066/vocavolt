from django.urls import path

from pages import views

app_name = "pages"


urlpatterns = [
    path('privacy-policy/', views.PrivacyPolicyPageView.as_view(), name="privacy_policy"),
    path('tos/', views.TermsOfServicePageView.as_view(), name="tos"),
]
