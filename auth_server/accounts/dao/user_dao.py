from accounts.models import User
from datetime import datetime
from django.db.models import Q


class UserDAO:
    @staticmethod
    def get_user_by_username(username):
        users = User.objects.filter(username = username)
        if not users.exists():
            return None
        return users[0]
    
    @staticmethod
    def get_users_by_email(email):
        users = User.objects.filter(email = email)
        if not users.exists():
            return None
        return users
    
    @staticmethod
    def create_user(username, password, first_name, last_name, email, is_staff=False, is_active=False, is_superuser=False):
        user = User(
            username = username,
            first_name = first_name,
            last_name = last_name,
            email = email,
            is_staff = is_staff,
            is_active = is_active,
            date_joined = datetime.now()
        )
        user.set_password(password)
        user.save()
        return user
    
    @staticmethod
    def get_users(
        user_id=None,
        username=None,
        email=None,
        first_name=None,
        last_name=None,
        is_staff=None,
        is_active=None,
        is_superuser=None,
    ):
        filters = Q()

        if user_id is not None:
            filters &= Q(id=user_id)

        if username:
            filters &= Q(username__icontains=username)

        if email:
            filters &= Q(email__icontains=email)

        if first_name:
            filters &= Q(first_name__icontains=first_name)

        if last_name:
            filters &= Q(last_name__icontains=last_name)

        if is_staff is not None:
            filters &= Q(is_staff=is_staff)

        if is_active is not None:
            filters &= Q(is_active=is_active)

        if is_superuser is not None:
            filters &= Q(is_superuser=is_superuser)
        return User.objects.filter(filters).order_by('id').values(
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "is_staff",
            "is_active",
            "is_superuser",
            "date_joined",
            "last_login"
        )