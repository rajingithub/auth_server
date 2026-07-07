from accounts.models import User
from datetime import datetime


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