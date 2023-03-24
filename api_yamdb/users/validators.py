import re

from rest_framework.serializers import ValidationError

from api_yamdb.settings import FORBIDDEN_USERNAMES


def validate_username(username):
    if username.lower() in FORBIDDEN_USERNAMES:
        raise ValidationError(
            f'"{username}" нельзя использовать в качестве имени пользователя!'
        )
    if not re.match(r'[\w.@+-]+\Z', username):
        raise ValidationError(
            f'{username} содержит запрещенные символы!'
            'Можно использовать только буквы, цифры и "@.+-_"'
        )
    return username
