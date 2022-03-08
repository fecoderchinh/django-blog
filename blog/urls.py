from django.urls import path, include
from . import views

from django.views.generic import RedirectView

app_name = 'main'
urlpatterns = [
    path(r'favicon\.ico', RedirectView.as_view(url='/static/favicon.ico')),
    path(r'', views.index, name='index'),
]