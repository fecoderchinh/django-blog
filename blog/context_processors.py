# -*- coding: utf-8 -*-
import django
django.setup()
from .models import SiteSettings


def load_settings(request):
    return {'site_settings': SiteSettings.load(), }
