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