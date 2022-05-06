from datetime import date

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from django.core import validators

from parler.models import TranslatableModel, TranslatedFields

from django_editorjs_fields import EditorJsJSONField


class PostAuthor(models.Model):
    """
    Model representing a blogger.
    """
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    # Read more about One-to-one relationships at https://docs.djangoproject.com/en/4.0/topics/db/examples/one_to_one/

    bio = models.TextField(max_length=400, help_text=_("Enter your bio details here."))

    class Meta:
        ordering = ["user", "bio"]
        verbose_name = _('Post Author')
        verbose_name_plural = _('Post Authors')
        db_table = 'authors'

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


class Category(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(max_length=255),
        description=models.TextField()
    )

    slug = models.SlugField(max_length=40, unique=True)

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        db_table = 'categories'

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


class Post(TranslatableModel):
    """
    Model representing a blog post.
    """
    translations = TranslatedFields(
        name=models.CharField(max_length=200),
        # description=models.TextField(max_length=2000, help_text=_("Enter your post content text here.")),
        description=EditorJsJSONField(readOnly=False, autofocus=True,
            i18n={
                'messages': {
                    'blockTunes': {
                        "delete": {
                            "Delete": _('Delete')
                        },
                        "moveUp": {
                            "Move up": _('Move up')
                        },
                        "moveDown": {
                            "Move down": _('Move down')
                        }
                    }
                },
            },
        ),
    )
    slug = models.SlugField(max_length=40, unique=True)
    author = models.ForeignKey(PostAuthor, on_delete=models.SET_NULL, null=True)
    # Foreign Key used because Post can only have one author/User, but bloggers can have multiple Posts.
    # Read more about Many-to-one relationships at https://docs.djangoproject.com/en/4.0/topics/db/examples/many_to_one/

    categories = models.ManyToManyField(Category, blank=True, null=True, through='CategoryToPost')
    # FYI: ManyToManyField.through
    # Read more at https://docs.djangoproject.com/en/4.0/ref/models/fields/#django.db.models.ManyToManyField.through

    post_date = models.DateField(default=date.today())

    class Meta:
        db_table = 'posts'
        ordering = ['-post_date']
        # The negative sign in front of "-post_date" indicates descending order.
        # Read more at https://docs.djangoproject.com/en/4.0/ref/models/querysets/#order-by-fields
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')

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
        db_table = 'post_comments'
        ordering = ['post_date']
        verbose_name = _('Post Comment')
        verbose_name_plural = _('Post Comments')

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


class CustomText(models.Model):
    name = models.SlugField()
    plain_text = models.TextField("Plain/Markdown Text", blank=True)
    html_text = models.TextField("HTML Text", blank=True)
    auto_render = models.BooleanField("Render to HTML using Markdown (on save)", default=True)

    class Meta:
        db_table = 'site_description'
        verbose_name = _('Description')
        verbose_name_plural = _('Descriptions')


class CustomImage(models.Model):
    name = models.SlugField()
    description = models.TextField("Description", null=True, blank=True)
    image = models.ImageField("Custom Image", upload_to="uploads/images/", null=True, blank=True)

    class Meta:
        db_table = 'site_identity'
        verbose_name = _('Image')
        verbose_name_plural = _('Images')


class Menu(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'menu'
        verbose_name = _('Menu')
        verbose_name_plural = _('Menus')

    def __unicode__(self):
        return self.name

    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.name


class MenuItem(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=100)
    order = models.CharField(blank=True, null=True, max_length=10)
    parent = models.ForeignKey('self', blank=True, null=True, related_name='child', on_delete=models.CASCADE)

    class Admin:
        list_display = ('name', '_parents_repr')

    def __str__(self):
        p_list = self._recurse_for_parents(self)
        p_list.append(self.name)
        return self.get_separator().join(p_list)

    def get_absolute_url(self):
        return self.url

    def _recurse_for_parents(self, cat_obj):
        p_list = []
        if cat_obj.parent_id:
            p = cat_obj.parent
            p_list.append(p.name)
            more = self._recurse_for_parents(p)
            p_list.extend(more)
        if cat_obj == self and p_list:
            p_list.reverse()
        return p_list

    def get_separator(self):
        return ' :: '

    def _parents_repr(self):
        p_list = self._recurse_for_parents(self)
        return self.get_separator().join(p_list)

    _parents_repr.short_description = "Tag parents"

    def save(self):
        p_list = self._recurse_for_parents(self)
        if self.name in p_list:

            raise validators.ValidationError("You must not save a category in itself!")
        super(MenuItem, self).save()

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('order',)
        db_table = 'menu_item'
        verbose_name = _('Item')
        verbose_name_plural = _('Items')
