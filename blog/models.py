from django.db import models


def get_absolute_url():
    from django.urls import reverse
    # return reverse('article-detail', args=(str(self.id)))
    return reverse('home')


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title
