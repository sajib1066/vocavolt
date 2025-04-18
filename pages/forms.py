from django import forms
from django.core.exceptions import ValidationError

from .models import Contact


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 rounded border border-gray-300 bg-white text-black focus:outline-none focus:ring-2 focus:ring-yellow-400',
                'placeholder': 'Your name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-2 rounded border border-gray-300 bg-white text-black focus:outline-none focus:ring-2 focus:ring-yellow-400',
                'placeholder': 'Your email'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 rounded border border-gray-300 bg-white text-black focus:outline-none focus:ring-2 focus:ring-yellow-400',
                'placeholder': 'Subject (optional)'
            }),
            'message': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 rounded border border-gray-300 bg-white text-black focus:outline-none focus:ring-2 focus:ring-yellow-400',
                'rows': 5,
                'placeholder': 'Your message...'
            }),
        }
    
    def clean_message(self):
        message = self.cleaned_data.get('message', '')
        word_count = len(message.split())
        if word_count > 250:
            raise ValidationError("Message cannot exceed 250 words. You entered {} words.".format(word_count))
        return message
