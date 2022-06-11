from django.urls import path, include
from . import views

from django.views.generic import RedirectView

app_name = 'main'
urlpatterns = [
    path(r'favicon\.ico', RedirectView.as_view(url='/static/favicon.ico')),
    path(r'', views.index, name='index'),
    path(r'blog/', views.PostList.as_view(), name='blog-list'),
    path(r'blog/<slug:slug>/', views.PostDetail.as_view(), name='blog-detail'),
    path(r'upload-image', views.ImageUploadView.as_view(), name='image_upload'),
    path(r'delete-image', views.remove_image, name='image_remove'),
]
