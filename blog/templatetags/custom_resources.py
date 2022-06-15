from django import template
from django.utils.safestring import mark_safe

from blog.models import MenuItem

register = template.Library()


# @register.simple_tag
# def custom_image(image_name):
#     cimage = CustomImage.objects.filter(name=image_name).first()
#     return cimage.image.url if cimage else "custom_image_%s_not_found" % image_name
#
#
# @register.simple_tag
# @mark_safe
# def custom_text(text_name):
#     text = CustomText.objects.filter(name=text_name).first()
#     return text.html_text if text else "Custom text <%s> not found." % text_name


@register.inclusion_tag('includes/main_menu.html')
def get_main_menu():
    return {'menu': MenuItem.objects.filter(menu__name='main').filter(parent__isnull=True)}
