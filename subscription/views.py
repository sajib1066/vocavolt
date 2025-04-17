from django.views.generic import View
from django.shortcuts import render

from subscription.models import SubscriptionPlan


class PricingPageView(View):
    """ Pricing view """
    template_name = 'subscription/plan.html'

    def get(self, request, *args, **kwargs):
        plans = SubscriptionPlan.objects.all()
        context = {
            'plans': plans,
        }
        return render(request, self.template_name, context)
