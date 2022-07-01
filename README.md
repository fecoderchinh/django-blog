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

Run `py .\manage.py collectstatic` to collect static files from each of your applications (and any other places you specify) into a single location that can easily be served in production.

---
For more Tutorials, you may also want to visit [This Page](https://github.com/fecoderchinh/django-blog/blob/master/docs/index.md).