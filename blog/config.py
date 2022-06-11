from secrets import token_urlsafe

from django.conf import settings

IMAGE_UPLOAD_PATH = str(
    getattr(settings, "EDITORJS_IMAGE_UPLOAD_PATH", 'uploads/images/')
)

IMAGE_UPLOAD_PATH_DATE = getattr(
    settings, "EDITORJS_IMAGE_UPLOAD_PATH_DATE", '%Y/%m/')

IMAGE_NAME_ORIGINAL = getattr(
    settings, "EDITORJS_IMAGE_NAME_ORIGINAL", False)

IMAGE_NAME = getattr(
    settings, "EDITORJS_IMAGE_NAME", lambda **_: token_urlsafe(8))