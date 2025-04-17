from django.utils import timezone
from django.db.models import Count
from django.views import View
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Quiz, UserQuizAttempt, Question

class QuizListView(View):
    template_name = 'quizzes/quizzes.html'

    def get(self, request, *args, **kwargs):
        now = timezone.now()
        active_quiz = Quiz.objects.filter(end_date__gt=now).order_by('end_date').first()
        finished_quizzes = Quiz.objects.filter(end_date__lte=now).order_by('-end_date')

        # Add stats for finished quizzes
        finished_quizzes_data = []
        for quiz in finished_quizzes:
            participants = UserQuizAttempt.objects.filter(quiz=quiz).count()
            top_performers = (
                UserQuizAttempt.objects
                .filter(quiz=quiz)
                .select_related('user')
                .order_by('-score')[:3]
            )
            finished_quizzes_data.append({
                'quiz': quiz,
                'participants': participants,
                'top_performers': top_performers,
            })

        context = {
            'active_quiz': active_quiz,
            'finished_quizzes': finished_quizzes_data,
        }
        return render(request, self.template_name, context)


class QuizView(LoginRequiredMixin, View):
    template_name = 'quizzes/quiz.html'

    def get(self, request, *args, **kwargs):
        quiz = Quiz.objects.get(pk=self.kwargs.get('pk'))
        # Get all questions related to the quiz
        questions = Question.objects.filter(quiz=quiz)
        
        # Pass the quiz and questions to the context
        context = {
            'quiz': quiz,
            'questions': questions
        }
        return render(request, self.template_name, context)
