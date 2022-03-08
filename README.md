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
django-crispy-forms
django-rosetta
```
Run `pip install -r .\setup.txt` to build all packages inside the setup.txt

---
## Tutorials
#### Writing a first view
Run `py manage.py startapp blog` to create new app in your project
***
### view
```pycon
from django.shortcuts import render

def index(request):
    return render(request, 'blog/index.html')
```
Note: Before we can render the view, we should add the app name into `settings > [INSTALLED_APPS]` to override its templates directory.
```pycon
INSTALLED_APPS = [
    ...,
    'blog',
    ...,
]
```
***
### url

Step 1: Add the group url for your app in `project > urls.py`
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
Step 2: Create new `urls.py` inside your app and add url for each view.
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