from django.urls import path

from subscription import views

app_name = "subscription"


urlpatterns = [
    path("pricing/", views.PricingPageView.as_view(), name="pricing"),
]
