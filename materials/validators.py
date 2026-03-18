from django.core.exceptions import ValidationError


def validate_youtube(value):
    if "youtube.com" not in value and "youtu.be" not in value:
        raise ValidationError("Это не ссылка на Youtube!")