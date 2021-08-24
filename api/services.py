from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework.generics import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken

from api.models import User


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'access': str(refresh.access_token),
        'refresh': str(refresh),
    }


def send_email_to_user(email, code):
    send_mail(
        'API Authentication',
        f'Your confirmation code {code}',
        'api@api.ru',
        [email]
    )


def validate_serializer(serializer_class, data):
    serializer = serializer_class(data=data)
    serializer.is_valid(raise_exception=True)

    return serializer


def get_or_create_user(email):
    user, _ = User.objects.get_or_create(email=email)
    return user


def generate_confirmation_code(email):
    user = get_or_create_user(email)
    return default_token_generator.make_token(user)


def check_confirmation_code(email, code):
    user = get_or_create_user(email)
    return user, default_token_generator.check_token(user, code)
