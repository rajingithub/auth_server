from oauth2_provider.models import Application


class ApplicationDAO:
    @staticmethod
    def create_application(
            application_name,
            user,
            redirect_uris,
            client_type,
            grant_type,
            client_secret
    ):
        application = Application.objects.create(
            name=application_name,
            user=user,
            redirect_uris=redirect_uris,
            client_type=client_type,
            authorization_grant_type=grant_type,
            client_secret=client_secret
        )
        return application

    @staticmethod
    def get_application_by_client_id(client_id):       
        application = Application.objects.filter(client_id=client_id)
        if application.exists():
            return application.first()
        else:
            return None