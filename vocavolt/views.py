from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
from django.utils import timezone
import json

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required



from flashcards.models import Section, WordPack, Quiz, Question, Word, UserWordProgress

class HomePageView(View):
    """ Home view """
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, self.template_name, context)



class SectionsPageView(LoginRequiredMixin, View):
    """ Home view """
    template_name = 'sections.html'

    def get(self, request, *args, **kwargs):
        sections = Section.objects.all().order_by('order')  # Make sure sections are ordered
        section_data = []# First section should be unlocked

        for section in sections:
            wordpacks = WordPack.objects.filter(section=section)
            all_words = Word.objects.filter(word_pack__in=wordpacks)
            total_words = all_words.count()

            completed_words = UserWordProgress.objects.filter(
                user=request.user,
                word__in=all_words
            ).count()

            is_completed = total_words > 0 and completed_words == total_words
            progress_percentage = int((completed_words / total_words) * 100) if total_words else 0

            section_data.append({
                'pk': section.pk,
                'title': section.title,
                'description': section.description,
                'completed': is_completed,
                'completed_words': completed_words,
                'total_words': total_words,
                'progress_percentage': progress_percentage,
            })

        context = {
            'sections': section_data
        }
        return render(request, self.template_name, context)



class LearningPageView(LoginRequiredMixin, View):
    """ Home view """
    template_name = 'learning.html'

    def get(self, request, *args, **kwargs):
        section = Section.objects.get(pk=self.kwargs.get('pk'))
        wordpacks = WordPack.objects.filter(section=section).order_by('order')
        quizes = Quiz.objects.filter(section=section).order_by('order')

        learning_path = []
        previous_completed = True  # First item is always unlocked

        for index, wordpack in enumerate(wordpacks):
            all_words = Word.objects.filter(word_pack=wordpack)
            total_words = all_words.count()

            completed_count = UserWordProgress.objects.filter(
                user=request.user,
                word__in=all_words
            ).count()

            is_wordpack_completed = completed_count == total_words and total_words > 0
            progress_percentage = int((completed_count / total_words) * 100) if total_words else 0

            learning_path.append({
                'type': 'word_pack',
                'title': wordpack.title,
                'desc': wordpack.description,
                'number': index + 1,
                'url': 'flashcard',
                'pk': wordpack.pk,
                'completed': is_wordpack_completed,
                'locked': not previous_completed,
                'progress': progress_percentage,
                'completed_words': completed_count,
                'total_words': total_words,
            })

            previous_completed = is_wordpack_completed  # For the next quiz

            if index < len(quizes):
                quiz = quizes[index]

                # You can later check actual quiz completion status here
                is_quiz_completed = False  # Placeholder

                learning_path.append({
                    'type': 'quiz',
                    'title': quiz.title,
                    'desc': f'Test your {wordpack.title} knowledge',
                    'number': f'Q{index + 1}',
                    'url': 'quiz',
                    'pk': quiz.pk,
                    'completed': is_quiz_completed,
                    'locked': not previous_completed,
                    'progress': 0,
                    'completed_words': 0,
                })

                previous_completed = is_quiz_completed  # Next wordpack depends on this

        context = {
            'section': section,
            'learning_path': learning_path,
        }
        return render(request, self.template_name, context)




class FlashCardPageView(LoginRequiredMixin, View):
    """ Home view """
    template_name = 'flashcard.html'

    def get(self, request, *args, **kwargs):
        wordpack = WordPack.objects.get(pk=self.kwargs.get('pk'))
        words = Word.objects.filter(word_pack=wordpack)

        # Get all completed words for this user in this wordpack
        progress_word_ids = set(
            UserWordProgress.objects.filter(user=request.user, word__in=words).values_list('word_id', flat=True)
        )

        # Build flashcard list with completion status
        all_flashcards = []
        for word in words:
            all_flashcards.append({
                "word": word.word,
                "id": word.id,
                "part_of_speech": word.part_of_speech,
                "translation": word.translation,
                "examples": word.examples if hasattr(word, 'examples') else [],
                "completed": word.id in progress_word_ids
            })

        # Determine the index
        if "index" in request.GET:
            try:
                index = int(request.GET.get("index", 0))
            except ValueError:
                index = 0
            index = max(0, min(index, len(all_flashcards) - 1))
        else:
            # Default to first uncompleted word
            index = next((i for i, card in enumerate(all_flashcards) if not card["completed"]), 0)

        current_flashcard = all_flashcards[index] if all_flashcards else None

        context = {
            "wordpack": wordpack,
            "flashcards": {
                "list": all_flashcards,
                "current": current_flashcard,
            },
            "current_index": index,
            "total_flashcards": len(all_flashcards)
        }
        return render(request, self.template_name, context)


class QuizPageView(LoginRequiredMixin, View):
    """Quiz page view"""
    template_name = 'quiz.html'

    def get(self, request, *args, **kwargs):
        # Get the quiz using the pk passed in the URL
        quiz = Quiz.objects.get(pk=self.kwargs.get('pk'))
        
        # Get all questions related to the quiz
        questions = Question.objects.filter(quiz=quiz)
        
        # Pass the quiz and questions to the context
        context = {
            'quiz': quiz,
            'questions': questions
        }
        return render(request, self.template_name, context)


@csrf_exempt  # Use this if CSRF token is not included or to handle the CSRF manually
@login_required  # Ensure the user is logged in before updating progress
def update_word_progress(request):
    if request.method == "POST":
        try:
            # Get the word ID from the request body
            data = json.loads(request.body)
            word_id = data.get("word_id")
            print("word id", word_id)
            # Check if the word_id exists and is valid
            if not word_id:
                return JsonResponse({"error": "No word ID provided"}, status=400)

            # Update the user's progress for the word (assuming a model for user progress)
            user = request.user
            progress, created = UserWordProgress.objects.get_or_create(user=user, word_id=word_id)

            # Optionally, you can update progress status (e.g., mark as learned, etc.)
            progress.status = 'learned'  # Or any other status you have
            progress.save()

            return JsonResponse({"success": "Progress updated successfully"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)
