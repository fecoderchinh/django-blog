import os
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views import generic, View
from django.utils.translation import get_language, activate
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _

from rest_framework.decorators import api_view
from rest_framework import status

from django.core.files.storage import default_storage

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


def is_member(user):
    return user.groups.filter(name='Blogger').exists()


@login_required
@user_passes_test(is_member)
@api_view(['POST'])
def remove_image(request):
    # print('hello')
    # return Response({'message':request.POST.get('imagePath')})
    path_file = request.POST.get('image')
    # path_file = str(kwargs['imagePath'])

    if not path_file:
        return Response({'status': 0, 'message': 'Parameter "image" Not Found'})

    base_dir = getattr(settings, "BASE_DIR", '')
    path_file = f'{base_dir}{path_file}'

    if not os.path.isfile(path_file):
        return Response({'status': 0, 'message': 'File Not Found'})

    os.remove(path_file)

    return Response({'status': 1})


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_member), name='dispatch')
class ImageDeleteView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    @api_view(['POST'])
    def get(request):
        path_file = request.GET.get('imagePath')
        # path_file = str(kwargs['imagePath'])

        if not path_file:
            return Response({'success': 0, 'message': 'Parameter "pathFile" Not Found'})

        base_dir = getattr(settings, "BASE_DIR", '')
        path_file = f'{base_dir}{path_file}'

        if not os.path.isfile(path_file):
            return Response({'success': 0, 'message': 'File Not Found'})

        os.remove(path_file)

        return Response({'success': 1})
