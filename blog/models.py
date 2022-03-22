from datetime import date

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class PostAuthor(models.Model):
    """
    Model representing a blogger.
    """
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    # Read more about One-to-one relationships at https://docs.djangoproject.com/en/4.0/topics/db/examples/one_to_one/

    bio = models.TextField(max_length=400, help_text=_("Enter your bio details here."))

    class Meta:
        ordering = ["user", "bio"]

    def get_absolute_url(self):
        """
        Returns the url to access a particular post-author instance.
        """
        return reverse('posts-by-author', args=[str(self.id)])

    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=40, unique=True)
    description = models.TextField()

    class Meta:
        verbose_name_plural = "Categories"

    def get_absolute_url(self):
        """
        Returns the url to access a particular category instance.
        """
        return reverse('posts-by-category', args=[str(self.slug)])

    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.name


class Post(models.Model):
    """
    Model representing a blog post.
    """
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=40, unique=True)
    author = models.ForeignKey(PostAuthor, on_delete=models.SET_NULL, null=True)
    # Foreign Key used because Post can only have one author/User, but bloggers can have multiple Posts.
    # Read more about Many-to-one relationships at https://docs.djangoproject.com/en/4.0/topics/db/examples/many_to_one/

    categories = models.ManyToManyField(Category, blank=True, null=True, through='CategoryToPost')
    # FYI: ManyToManyField.through
    # Read more at https://docs.djangoproject.com/en/4.0/ref/models/fields/#django.db.models.ManyToManyField.through

    description = models.TextField(max_length=2000, help_text=_("Enter your post content text here."))
    post_date = models.DateField(default=date.today())

    class Meta:
        ordering = ['-post_date']
        # The negative sign in front of "-post_date" indicates descending order.
        # Read more at https://docs.djangoproject.com/en/4.0/ref/models/querysets/#order-by-fields

    def get_absolute_url(self):
        """
        Returns the url to access a particular post instance.
        """
        return reverse('post-detail', args=[str(self.slug)])

    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.name


class CategoryToPost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class PostComment(models.Model):
    """
    Model representing a comment against a blog post.
    """
    description = models.TextField(max_length=1000, help_text=_("Enter comment about blog here."))
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    # Foreign Key used because PostComment can only have one author/User, but users can have multiple comments
    # Read more about Many-to-one relationships at https://docs.djangoproject.com/en/4.0/topics/db/examples/many_to_one/

    post_date = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        ordering = ['post_date']

    def __str__(self):
        """
        String for representing the Model object.
        """
        len_title = 75
        if len(self.description) > len_title:
            title_string = self.description[:len_title] + '...'
        else:
            title_string = self.description
        return title_string
