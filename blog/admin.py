from django.contrib import admin
from django import forms
from django.db.models import fields
from django.db.utils import ProgrammingError
from .models import (
    Category,
    Post,
    PostAuthor,
    PostComment,
    Menu,
    MenuItem,
    SiteSettings,
    Gallery,
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
    list_display = ('name', 'slug', 'post_date')
    exclude = ['author', ]
    inlines = [PostCommentsInline]

    def save_model(self, request, obj, form, change):
        if PostAuthor.objects.filter(user=request.user).exists():
            obj.author = PostAuthor.objects.get(user=request.user)
        else:
            PostAuthor.objects.create(user=request.user).save()
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
            'all': ('https://code.jquery.com/ui/1.13.1/themes/base/jquery-ui.css',)
        }


class MenuItemInline(admin.StackedInline):
    model = MenuItem
    extra = 0


admin.site.register(Menu,
                    inlines=[MenuItemInline],
                    form=MenuForm,
                    )


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    change_list_template = 'custom_templates/change_list.html'
    list_display = ['image_tag']

    class Media:
        js = (
            '/static/js/gallery-actions.js',
        )
        css = {
            'all': ('/static/css/gallery-admin.css',)
        }


class SiteSettingsAdmin(admin.ModelAdmin):
    # Create a default object on the first page of SiteSettingsAdmin with a list of settings
    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        # be sure to wrap the loading and saving SiteSettings in a try catch,
        # so that you can create database migrations
        try:
            SiteSettings.load().save()
        except ProgrammingError:
            pass

    class Media:
        js = (
            '/static/js/site_setting_actions.js',
        )

    # prohibit adding new settings
    def has_add_permission(self, request, obj=None):
        return False

    # as well as deleting existing
    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(SiteSettings, SiteSettingsAdmin)
