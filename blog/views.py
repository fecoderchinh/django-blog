import os
from datetime import datetime
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.module_loading import import_string
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

from .config import (IMAGE_NAME, IMAGE_NAME_ORIGINAL, IMAGE_UPLOAD_PATH,
                     IMAGE_UPLOAD_PATH_DATE)

from .models import Post, Gallery


def get_storage_class():
    return import_string(
        getattr(
            settings,
            'EDITORJS_STORAGE_BACKEND',
            'django.core.files.storage.DefaultStorage',
        )
    )()


class ImageUploadView(View):
    http_method_names = ["post"]

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        if 'image' in request.FILES:
            the_file = request.FILES['image']
            allowed_types = [
                'image/jpeg',
                'image/jpg',
                'image/pjpeg',
                'image/x-png',
                'image/png',
                'image/webp',
                'image/gif',
            ]
            if the_file.content_type not in allowed_types:
                return JsonResponse(
                    {'success': 0, 'message': 'You can only upload images.'}
                )

            filename, extension = os.path.splitext(the_file.name)

            if IMAGE_NAME_ORIGINAL is False:
                filename = IMAGE_NAME(filename=filename, file=the_file)

            filename += extension

            upload_path = IMAGE_UPLOAD_PATH

            if IMAGE_UPLOAD_PATH_DATE:
                upload_path += datetime.now().strftime(IMAGE_UPLOAD_PATH_DATE)

            path = get_storage_class().save(
                os.path.join(upload_path, filename), the_file
            )
            link = get_storage_class().url(path)
            Gallery.objects.create(path=path).save()

            return JsonResponse({'success': 1, 'file': {"url": link}})
        return JsonResponse({'success': 0})


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
