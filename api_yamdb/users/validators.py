from rest_framework.serializers import ValidationError


def validate_username(value):
    if value.lower() == 'me':
        raise ValidationError(
            '"Me" не может использоваться в качестве имени пользователя!'
        )
    return value
