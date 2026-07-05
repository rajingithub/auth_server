import os
import binascii
from datetime import datetime, timedelta
from utils.logger import logger
from accounts.helper.authentication_backend import UsernameAuthBackend, EmailAuthBackend
from accounts.dao.access_token_dao import AccessTokenDAO
from auth_server.settings import ACCESS_TOKEN_SIZE, ACCESS_TOKEN_EXPIRY_IN_SECS


AUTH_BACKENDS = [
    UsernameAuthBackend,
    EmailAuthBackend
]


def random_token_generator(size):
    return binascii.hexlify(os.urandom(size)).decode()


class AuthViewHelper:
    @staticmethod
    def authenticate_user(user_identifier, password):
        # user is identified by either username/email which will be sent in the
        # same parameter name : user_identifier 
        user_authenticated = False
        user = None
        for backend in AUTH_BACKENDS:
            user, error = backend.authenticate(user_identifier=user_identifier, password = password)
            if user:
                user_authenticated = True
                break
        
        if not user_authenticated or not user:
            err_msg = "unable to authenticate user"
            logger.error(f"{err_msg}", extra={"user_identifier":user_identifier})
            return None, err_msg
        token = random_token_generator(size = ACCESS_TOKEN_SIZE)
        access_token = AccessTokenDAO.create_access_token(
            token=token,
            expiry=datetime.now() + timedelta(seconds=ACCESS_TOKEN_EXPIRY_IN_SECS),
            user = user,
        )
        return {
            "user_id" : user.id,
            "access_token" : access_token.token,
            "expires_in_secs" : ACCESS_TOKEN_EXPIRY_IN_SECS,
            "token_type" : "Bearer" 
        }, None
        

    @staticmethod
    def authenticate_client_credentials(client_id, client_secret):
        pass

