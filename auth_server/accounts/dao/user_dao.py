from accounts.models import User


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
    