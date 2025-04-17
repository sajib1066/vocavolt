from django.db import models

from customauth.models import User


class Quiz(models.Model):
    title = models.CharField(max_length=100)
    instructions = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()

    def __str__(self):
        return self.title


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    prompt = models.TextField()
    options = models.JSONField()  # Store list like ["Option A", "Option B", ...]
    correct_answer = models.CharField(max_length=255)

    def __str__(self):
        return f"Question for {self.quiz.title}"

class UserQuizAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_quiz")
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    score = models.IntegerField(default=0)

    @property
    def total_questions(self):
        return self.answers.count()

    @property
    def total_correct_answers(self):
        return self.answers.filter(is_correct=True).count()

    @property
    def calculate_score_percentage(self):
        total_questions = self.answers.count()
        correct_answers = self.answers.filter(is_correct=True).count()

        if total_questions == 0:
            return 0  # Avoid division by zero

        return int((correct_answers / total_questions) * 100)


class UserAnswer(models.Model):
    attempt = models.ForeignKey(UserQuizAttempt, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.CharField(max_length=255)
    is_correct = models.BooleanField()
