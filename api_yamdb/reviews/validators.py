from django.core.exceptions import ValidationError
from django.utils import timezone


def year(value):
    if value > timezone.now().year:
        raise ValidationError(
            'Год создания произвеодения не может быть больше текущего'
        )
