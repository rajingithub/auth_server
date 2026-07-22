
import secrets
from accounts.dao.application_dao import ApplicationDAO
from accounts.dao.user_dao import UserDAO

class ApplicationViewHelper:
    @staticmethod
    def create_application(application_name, user_id, redirect_uris, client_type, grant_type):
        try:
            user = UserDAO.get_user_by_id(user_id)
            client_secret = secrets.token_urlsafe(32)
            application = ApplicationDAO.create_application(
                application_name=application_name,
                user=user,
                redirect_uris=redirect_uris,
                client_type=client_type,
                grant_type=grant_type,
                client_secret=client_secret
            )
            return {
                "application_id": application.id,
                "client_id": application.client_id,
                "client_secret": application.client_secret
            }, None
        except Exception as e:
            return None, str(e)