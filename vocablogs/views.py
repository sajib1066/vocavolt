from django.views.generic import ListView, View
from django.shortcuts import render, get_object_or_404

from vocablogs.models import Category, Article


class ArticleListView(ListView):
    template_name = 'vocablogs/list.html'
    model = Article
    paginate_by = 15  # set as default pagination

    def get_queryset(self, **kwargs):
        objects = self.model.objects.filter(is_active=True)
        return objects

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(is_active=True)
        return context


class ArticleDetailsView(View):
    template_name = 'vocablogs/details.html'
    model = Article

    def get(self, request, *args, **kwargs):
        article = get_object_or_404(self.model, slug=self.kwargs['slug'])
        context = {
            'article': article,
        }
        return render(request, self.template_name, context)
