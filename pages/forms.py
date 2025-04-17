from django import forms
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
