import logging
from django.views.generic import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login
import uuid
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.urls import reverse

from customauth.forms import RegisterForm
from customauth.models import User
from customauth.send_mail import send_confirmation_email

logger = logging.getLogger(__name__)


class RegisterView(View):
    template_name = 'customauth/register.html'
    form_class = RegisterForm

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('sections')
        return render(request, self.template_name, {'form': self.form_class})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']

            if password != confirm_password:
                messages.warning(request, "Passwords do not match")
                return render(request, self.template_name, {'form': form})

            # Generate token and create user
            token = str(uuid.uuid4())
            user = User.objects.create_user(
                email=email,
                password=password,
                is_active=False,
                email_token=token
            )
            user.profile.name = name
            user.profile.save()

            # Build confirmation link
            confirm_url = request.build_absolute_uri(
                reverse('customauth:confirm_email', kwargs={'token': token})
            )

            # ✅ Use your reusable function
            send_confirmation_email(confirm_url, user)
            messages.success(request, "✅ We've sent you a confirmation email. Please check your inbox or spam folder to activate your account.")
            return redirect('customauth:login')

        messages.warning(request, 'There was a problem with your registration.')
        return render(request, self.template_name, {'form': form})


def confirm_email(request, token):
    user = get_object_or_404(User, email_token=token, is_active=False)

    user.is_active = True
    user.verified_email = True
    user.email_token = None  # Invalidate token
    user.save()
    login(request, user)
    messages.success(request, "Email confirmed! You can now log in.")
    return redirect('sections')
