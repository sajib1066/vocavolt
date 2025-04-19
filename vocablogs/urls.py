from django.urls import path

from vocablogs import views

app_name = 'vocablogs'


urlpatterns = [
    path('', views.ArticleListView.as_view(), name='list'),
    path('<str:slug>/', views.ArticleDetailsView.as_view(), name='details'),
]
