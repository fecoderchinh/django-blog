from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views import generic
from django.utils.translation import get_language, activate

from .models import Post


# Create your views here.
def index(request):
    return render(request, 'index.html')


class PostList(generic.ListView):
    model = Post
    template_name = 'blog/list.html'

    def get_queryset(self):
        return super().get_queryset().filter(translations__language_code=get_language())


class PostDetail(generic.DetailView):
    model = Post
    template_name = 'blog/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
