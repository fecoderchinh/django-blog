# Django 4.0 Sample Blog using SSR + CSR

### Resources
1. Django 4.0
2. DataTable (jQuery)
3. Django Rest Framework
4. Django Parler (imported Parler Rest within)

----
#### These details were based on [Django First App Tutorial](https://docs.djangoproject.com/en/4.0/intro/tutorial01/) and working on Windows.
#### Check for the version that installed on your machine.
Run `py -m django --version` to check for the current Django version.
### Creating a project
Run `django-admin startproject djangoBlog` at your root of project's directory.
### The development server
Run `py manage.py runserver`

---

### Create a setup.txt that includes the packages needs.

For this project, we have to add the below packages:
```text
pymysql
mysqlclient
django-crispy-forms
django-parler
djangorestframework
django-rosetta
django-sass
```
Run `pip install -r .\setup.txt` to build all packages inside the setup.txt

And don't forget to add these packages in your `settings.py`

```pycon
INSTALLED_APPS = [
    ...,
    'parler',
    'crispy_forms',
    'rest_framework',
    'rosetta',
    'django_sass',
    ...,
]
```

---
## Tutorials
#### Writing a first view
Run `py manage.py startapp blog` to create new app in your project
***
### view

```pycon
from django.shortcuts import render

def index(request):
    return render(request, 'blog/blog/templates/index.html')
```
**_Note:_** Before we can render the view, we should add the app name into `settings > [INSTALLED_APPS]` to override its templates directory.
```pycon
INSTALLED_APPS = [
    ...,
    'blog',
    ...,
]
```
Note: You can find and edit the app name in `apps.py`
***
### url

**_Step 1:_** Add the group url for your app in `project > urls.py`
<br>(In this case, our project is `blog`)
```pycon
...
from django.urls import include, path
...

urlpatterns = [
    ...,
    path(r'', include('blog.urls')),
    ...,
]
```
**_Step 2:_** Create new `urls.py` inside your app and add url for each view.
```pycon
from django.urls import path
from . import views

...

app_name = 'main'
urlpatterns = [
    ...
    path(r'', views.index, name='index'),
    ...,
]
```

***
### model
This project is working with MySQL, so the most important is make sure that we have run `pip install -r .\setup.txt` already.

#### Because we have included several mysql packages in the file.

**_Step 1:_** Adding database in your app
```pycon
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': DATABASE_NAME,
        'USER': DATABASE_USER,
        'PASSWORD': DATABASE_PASSWORD,
        'HOST': HOST_NAME,
        'PORT': HOST_PORT,
    }
}
```

**_Step 2:_** Create a simple models

```pycon
class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
```

_**Step 3:**_ 
- Run `py .\manage.py makemigrations` if you are updating current models.
- Run `py .\manage.py migrate` to add the django's models in your database.

**_Step 4:_** Run `py .\manage.py createsuperuser` to create admin user so that we can manage our admin site.

***
### multilingual
These tutorial will guide you to add multi-language in your project.

First, Make sure you have installed the below packages:
1. [django-parler](https://github.com/django-parler/django-parler/tree/577ca2f4a80713a9272c48db30e914a4d9332358)
2. [django-parler-rest](https://github.com/django-parler/django-parler-rest) (This is optional to combine with [djangorestframework](https://www.django-rest-framework.org/#installation))
3. [django-rosetta](https://github.com/mbi/django-rosetta) (Use to translate your content)

```commandline
pip install django-parler django-parler-rest django-rosetta
```
**_Step 1:_** Adding the configurations in the `settings.py`
```pycon
INSTALLED_APPS = [
    ...,
    'parler',
    'rosetta',
    ...,
]

MIDDLEWARE = [
    ...,
    'django.middleware.locale.LocaleMiddleware',
    ...,
]

LANGUAGES = (
    ('en', _('English')),
    ('vi', _('Vietnamese')),
)

LOCALE_PATHS = [
    BASE_DIR / 'locale/',
]

PARLER_LANGUAGES = {
    None: (
        {'code': 'en', },  # English
        {'code': 'vi', },  # Vietnamese
    ),
    'default': {
        'fallbacks': ['en'],
        'hide_untranslated': False,
    }
}
```
**_Step 2:_** Update the main `urls.py`
```pycon
from django.conf.urls.i18n import i18n_patterns

urlpatterns = i18n_patterns(
    ...,
    path(r'rosetta/', include('rosetta.urls')),
    ...,
)
```

**_Step 3:_** Specifying for the translation column in `models.py`
```pycon
from parler.models import TranslatableModel, TranslatedFields
from django.utils.translation import gettext_lazy as _

class Category(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(max_length=255),
        description=models.TextField()
    )
    
    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
    
    def __str__(self):
        return self.name
```

**_Step 4:_** Enable the translation table in `admin.py`

```pycon
from parler.admin import TranslatableAdmin

admin.site.register(Category, TranslatableAdmin)
```

**_Step 5:_** Create new folder `locale/` and add new folder for each language:
```text
locale
├── en
├── ...
└── vi
```

**_Step 6:_** Download a precompiled binary installer for [gettext on Windows](https://docs.djangoproject.com/en/4.0/topics/i18n/translation/#gettext-on-windows-1)

**_Step 7:_** Run `django-admin makemessages --all --ignore=venv` to create `*.po` files

**_Step 8:_** Run `django-admin compilemessages --ignore=venv` to compile messages

#### That's it, from now we can open the `.po` file and translate messages

#### We prefer to go to `http://127.0.0.1:8000/rosetta` and choose the language that we want to translate
***