from django import forms
from flashcards.models import WordPack


class WordCreateForm(forms.Form):
    word_pack = forms.ModelChoiceField(
        queryset=WordPack.objects.all().order_by('section'),
        widget=forms.Select(attrs={
            'class': 'mt-1 w-full px-4 py-2 rounded-md bg-gray-800 border border-gray-700 text-white'
        })
    )
    word = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'mt-1 w-full px-4 py-2 rounded-md bg-gray-800 border border-gray-700 text-white',
            'placeholder': 'Enter english word'
        })
    )
    part_of_speech = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'mt-1 w-full px-4 py-2 rounded-md bg-gray-800 border border-gray-700 text-white',
            'placeholder': 'e.g., noun, verb'
        })
    )
    translation = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'mt-1 w-full px-4 py-2 rounded-md bg-gray-800 border border-gray-700 text-white',
            'placeholder': 'Translation (বাংলা)'
        })
    )
    synonyms = forms.CharField(
        max_length=255, required=False,
        widget=forms.TextInput(attrs={
            'class': 'mt-1 w-full px-4 py-2 rounded-md bg-gray-800 border border-gray-700 text-white',
            'placeholder': 'Comma-separated synonyms'
        })
    )
    antonyms = forms.CharField(
        max_length=255, required=False,
        widget=forms.TextInput(attrs={
            'class': 'mt-1 w-full px-4 py-2 rounded-md bg-gray-800 border border-gray-700 text-white',
            'placeholder': 'Comma-separated antonyms'
        })
    )
    description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'mt-1 w-full px-4 py-2 rounded-md bg-gray-800 border border-gray-700 text-white',
            'placeholder': 'Optional description'
        })
    )

    # Take multiple example sentences
    example_1 = forms.CharField(
        max_length=200, required=False,
        widget=forms.TextInput(attrs={
            'class': 'mt-1 w-full px-4 py-2 rounded-md bg-gray-800 border border-gray-700 text-white',
            'placeholder': 'Example sentence 1'
        })
    )
    example_2 = forms.CharField(
        max_length=200, required=False,
        widget=forms.TextInput(attrs={
            'class': 'mt-1 w-full px-4 py-2 rounded-md bg-gray-800 border border-gray-700 text-white',
            'placeholder': 'Example sentence 2'
        })
    )
    example_3 = forms.CharField(
        max_length=200, required=False,
        widget=forms.TextInput(attrs={
            'class': 'mt-1 w-full px-4 py-2 rounded-md bg-gray-800 border border-gray-700 text-white',
            'placeholder': 'Example sentence 3'
        })
    )

    def get_examples_list(self):
        """Combine non-empty examples into a list"""
        return [e for e in [
            self.cleaned_data.get('example_1'),
            self.cleaned_data.get('example_2'),
            self.cleaned_data.get('example_3'),
        ] if e]
