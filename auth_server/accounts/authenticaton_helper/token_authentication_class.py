from datetime import datetime, timezone
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from accounts.dao.access_token_dao import AccessTokenDAO


class TokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        http_authorization = request.META.get('HTTP_AUTHORIZATION', "")
        if not http_authorization:
            raise AuthenticationFailed('No authentication token provided')
        token = http_authorization.split()[-1]
        if not token:
            raise AuthenticationFailed('No authentication token provided')
        access_token = AccessTokenDAO.get_access_token_details(token)
        if not access_token:
            raise AuthenticationFailed('Invalid authentication token')
        if access_token.expires < datetime.now(timezone.utc):
            raise AuthenticationFailed('Authentication token has expired')
        return (access_token.user, access_token)
