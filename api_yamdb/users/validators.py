from django.core.validators import RegexValidator
from rest_framework.serializers import ValidationError

from api_yamdb.settings import FORBIDDEN_USERNAMES


def validate_username(username):
    if username.lower() in FORBIDDEN_USERNAMES:
        raise ValidationError(
            f'"{username}" нельзя использовать в качестве имени пользователя!'
        )
    RegexValidator(regex='^[\\w.@+-]+\\Z').__call__(username)
    return username
