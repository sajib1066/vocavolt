from django.urls import path

from quizzes import views

app_name = "quizzes"


urlpatterns = [
    path('', views.QuizListView.as_view(), name="quizzes"),
    path("<int:pk>/", views.QuizView.as_view(), name="quiz"),
    path('submit-quiz-answer/', views.submit_quiz_result, name='submit_quiz_result'),
]
