from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib import messages

from pages.models import Contact
from pages.forms import ContactForm


class PrivacyPolicyPageView(View):
    """ Home view """
    template_name = 'pages/privacy_policy.html'

    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, self.template_name, context)


class TermsOfServicePageView(View):
    """ Home view """
    template_name = 'pages/terms.html'

    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, self.template_name, context)


class ContactPageView(View):
    """ Contact view """
    template_name = 'pages/contact.html'
    model = Contact
    form_class = ContactForm

    def get(self, request, *args, **kwargs):
        form = self.form_class
        context = {
            'form': form
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Your message has been sent successfully!")
            return redirect('pages:contact')
        context = {
            'form': form
        }
        return render(request, self.template_name, context)

def error_403_handler(request, *args, **argv):
    return render(request, 'pages/403.html')


def error_404_handler(request, *args, **argv):
    return render(request, 'pages/404.html')


def error_500_handler(request, *args, **argv):
    return render(request, 'pages/500.html')
