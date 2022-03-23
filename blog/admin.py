from django.contrib import admin
from .models import (
    Category,
    Post,
    PostAuthor,
    PostComment,
)

from parler.admin import TranslatableAdmin

admin.site.register(Category, TranslatableAdmin)
admin.site.register(PostAuthor)
admin.site.register(PostComment)


class PostCommentsInline(admin.TabularInline):
    """
    Used to show 'existing' blog comments inline below associated blogs
    """
    model = PostComment
    max_num = 0


@admin.register(Post)
class PostAdmin(TranslatableAdmin):
    """
    Administration objects for Blog models.
    Defines:
     - fields to be displayed in list view (list_display)
     - orders fields in detail view (fields), grouping the date fields horizontally
     - adds inline addition of blog comments in blog view (inlines)
    """
    list_display = ('name', 'slug', 'author', 'post_date')
    inlines = [PostCommentsInline]
