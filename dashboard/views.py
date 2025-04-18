from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from dashboard.forms import WordCreateForm
from flashcards.models import Word

class WordCreateView(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = 'dashboard/word_create.html'

    def test_func(self):
        # Only allow superusers
        return self.request.user.is_superuser

    def handle_no_permission(self):
        from django.http import HttpResponseForbidden
        return HttpResponseForbidden("You do not have permission to access this page.")

    def get(self, request):
        form = WordCreateForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = WordCreateForm(request.POST)
        if form.is_valid():
            Word.objects.create(
                word_pack=form.cleaned_data['word_pack'],
                word=form.cleaned_data['word'],
                part_of_speech=form.cleaned_data['part_of_speech'],
                translation=form.cleaned_data['translation'],
                synonyms=form.cleaned_data['synonyms'],
                antonyms=form.cleaned_data['antonyms'],
                description=form.cleaned_data['description'],
                examples=form.get_examples_list()
            )
            messages.success(request, "Word created successfully.")
            return redirect('dashboard:word_create')  # Update this as needed
        return render(request, self.template_name, {'form': form})
