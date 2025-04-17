import logging
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.urls import reverse
from django.utils.crypto import get_random_string

from customauth.forms import LoginForm
from customauth.send_mail import send_confirmation_email

logger = logging.getLogger(__name__)


class LoginView(LoginView):
    """ Custom login view """
    template_name = 'customauth/login.html'
    form_class = LoginForm

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('customauth:profile')
        form = self.form_class
        context = {
            'form': form,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        next_page = request.GET.get('next', '')
        form = self.form_class(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)

            if user:
                if not user.verified_email:
                    # Generate new token
                    user.email_token = get_random_string(length=64)
                    user.save()

                    # Create confirmation link
                    confirmation_link = request.build_absolute_uri(
                        reverse('customauth:confirm_email', args=[user.email_token])
                    )

                    # Send confirmation email
                    send_confirmation_email(confirmation_link, user)

                    messages.warning(request, 'Your email is not verified. A new confirmation link has been sent to your email.')
                    return render(request, self.template_name, {'form': form})

                # Email is verified — login user
                login(request, user)
                return redirect(next_page or 'customauth:profile')
            else:
                messages.warning(request, 'Invalid email or password')
        else:
            logger.error(f'Invalid form data: {form.errors}')
            messages.warning(request, 'Invalid email or password. Please enter correctly.')

        return render(request, self.template_name, {'form': form})
