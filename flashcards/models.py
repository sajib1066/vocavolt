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
