from django.contrib import admin
from django import forms
from .models import (
    Category,
    Post,
    PostAuthor,
    PostComment,
    CustomText,
    CustomImage,
    Menu,
    MenuItem,
)

from parler.admin import TranslatableAdmin

admin.site.register(Category, TranslatableAdmin)
admin.site.register(PostAuthor)
admin.site.register(PostComment)
admin.site.register(CustomText)
admin.site.register(CustomImage)


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
    list_display = ('name', 'slug', 'post_date')
    exclude = ['author', ]
    inlines = [PostCommentsInline]

    def save_model(self, request, obj, form, change):
        obj.author = PostAuthor.objects.get(user=request.user)
        super().save_model(request, obj, form, change)


class MenuForm(forms.ModelForm):
    model = Menu

    class Media:
        js = (
            'https://code.jquery.com/jquery-3.6.0.min.js',
            'https://cdnjs.cloudflare.com/ajax/libs/jqueryui/1.12.1/jquery-ui.min.js',
            '/static/js/menu-sort-stack-inline.js',
        )
        css = {
            'all': ('https://code.jquery.com/ui/1.13.1/themes/base/jquery-ui.css', )
        }


class MenuItemInline(admin.StackedInline):
    model = MenuItem
    extra = 0


admin.site.register(Menu,
                    inlines=[MenuItemInline],
                    form=MenuForm,
                    )
