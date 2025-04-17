from django.contrib import admin

from .models import Section, WordPack, Word, Quiz, Question, UserWordProgress, UserQuizAttempt, UserAnswer


class WordInline(admin.TabularInline):
    model = Word
    extra = 1


class WordPackInline(admin.TabularInline):
    model = WordPack
    extra = 1


class QuizInline(admin.TabularInline):
    model = Quiz
    extra = 1


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'order')
    inlines = [WordPackInline, QuizInline]
    ordering = ('order',)


@admin.register(WordPack)
class WordPackAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'section', 'order')
    list_filter = ('section',)
    search_fields = ('title',)
    inlines = [WordInline]
    ordering = ('section__order', 'order')


@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    list_display = ('id', 'word', 'part_of_speech', 'word_pack')
    list_filter = ('part_of_speech', 'word_pack__section')
    search_fields = ('word', 'translation')
    ordering = ('word_pack__section__order', 'word_pack__order')


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'section', 'order')
    list_filter = ('section',)
    search_fields = ('title',)
    inlines = [QuestionInline]
    ordering = ('section__order', 'order')


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'prompt', 'quiz')
    search_fields = ('prompt',)
    list_filter = ('quiz__section',)


@admin.register(UserWordProgress)
class UserWordProgressAdmin(admin.ModelAdmin):
    list_display = ['pk', 'user', 'word']


@admin.register(UserQuizAttempt)
class UserQuizAttemptAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'quiz']


@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ['id', 'attempt', 'question']
