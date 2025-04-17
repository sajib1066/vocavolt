from django.db import models

from customauth.models import User


class Section(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Section {self.order}: {self.title}"

    def get_absolute_url(self):
        return f'/section/{self.pk}/learn/'


class WordPack(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='wordpacks')
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Pack {self.order} in {self.section}"


class Word(models.Model):
    word_pack = models.ForeignKey(WordPack, on_delete=models.CASCADE, related_name='words')
    word = models.CharField(max_length=100)
    part_of_speech = models.CharField(max_length=50)
    translation = models.CharField(max_length=200)
    synonyms = models.CharField(max_length=255, blank=True, null=True)
    antonyms = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    examples = models.JSONField(default=list)  # Store as a list of example sentences

    def __str__(self):
        return self.word


class Quiz(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='quizzes')
    title = models.CharField(max_length=100)
    instructions = models.TextField(blank=True, null=True)
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Quiz {self.order} in {self.section}"


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    prompt = models.TextField()
    options = models.JSONField()  # Store list like ["Option A", "Option B", ...]
    correct_answer = models.CharField(max_length=255)

    def __str__(self):
        return f"Question for {self.quiz.title}"


class UserWordProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    last_studied = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.email} - {self.word.word}'


class UserQuizAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
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
