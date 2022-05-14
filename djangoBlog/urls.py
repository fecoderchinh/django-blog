"""djangoBlog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings
from django.conf.urls.static import static

import blog.views

urlpatterns = i18n_patterns(
    path('dashboard/', admin.site.urls),
    path('', include('blog.urls')),

    path(r'ua/', include("django.contrib.auth.urls")),
    path(r'favicon\.ico', RedirectView.as_view(url='/static/favicon/favicon-16.png')),
    path(r'rosetta/', include('rosetta.urls')),

    path('editorjs/', include('django_editorjs_fields.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
