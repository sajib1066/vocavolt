from django.utils import timezone
from django.db.models import Count
from django.views import View
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.utils import timezone
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from .models import Quiz, UserQuizAttempt, Question, UserAnswer

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


@csrf_exempt
@login_required
def submit_quiz_result(request):
    if request.method == 'POST' and request.user.is_authenticated:
        data = json.loads(request.body.decode('utf-8'))
        
        quiz_id = data.get('quiz_id')
        score = data.get('score')
        answers = data.get('answers')

        quiz = Quiz.objects.get(pk=quiz_id)
        attempt = UserQuizAttempt.objects.create(
            user=request.user,
            quiz=quiz,
            score=score,
            completed_at=timezone.now()
        )

        for answer in answers:
            question = Question.objects.get(pk=answer['question_id'])
            UserAnswer.objects.create(
                attempt=attempt,
                question=question,
                selected_option=answer['selected_option'],
                is_correct=(answer['selected_option'] == question.correct_answer)
            )

        return JsonResponse({'success': True, 'message': 'Result stored successfully.'})
    return JsonResponse({'success': False, 'message': 'Invalid request.'}, status=400)
