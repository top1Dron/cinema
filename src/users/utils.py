from users.models import User


def get_user_by_email(email):
    try:
        user = User.objects.get(email=email)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    return user