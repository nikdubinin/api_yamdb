import uuid

from django.core.mail import send_mail

from api_yamdb import settings


def send_confirmation_code(username: str, email: str, **kwargs) -> None:
    confirmation_code = kwargs.pop(
        'confirmation_code',
        str(uuid.uuid3(uuid.NAMESPACE_DNS, username))
    )
    send_mail(
        'Код подтверждения',
        f'Ваш код подтверждения: {confirmation_code}',
        settings.DEFAULT_FROM_EMAIL,
        [f'{email}'],
        fail_silently=False,
    )
