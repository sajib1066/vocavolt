from django.views.generic import View
from django.shortcuts import render


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
