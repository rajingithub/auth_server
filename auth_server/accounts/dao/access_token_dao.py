
from oauth2_provider.models import AccessToken
from auth_server.settings import OAUTH_PROVIDER_SCOPES

class AccessTokenDAO:    
    @staticmethod
    def create_access_token(
            token,
            expiry,
            user,
            application_id = None,
    ):
        
        scopes = OAUTH_PROVIDER_SCOPES
        access_token = AccessToken.objects.create(
            token = token,
            expires = expiry,
            scope = scopes,
            application_id = application_id,
            user = user
        )
        return access_token