import os
import base64
import binascii
from datetime import datetime, timedelta
from utils.logger import logger
from django.contrib.auth.hashers import check_password
from accounts.helper.authentication_backend import UsernameAuthBackend, EmailAuthBackend
from accounts.dao.access_token_dao import AccessTokenDAO
from accounts.dao.application_dao import ApplicationDAO
from auth_server.settings import ACCESS_TOKEN_SIZE, ACCESS_TOKEN_EXPIRY_IN_SECS


AUTH_BACKENDS = [
    UsernameAuthBackend,
    EmailAuthBackend
]


def random_token_generator(size):
    return binascii.hexlify(os.urandom(size)).decode()


class AuthViewHelper:
    @staticmethod
    def authenticate_user(user_identifier, password, client_id):
        # user is identified by either username/email which will be sent in the
        # same parameter name : user_identifier 
        application = ApplicationDAO.get_application_by_client_id(client_id)
        if not application:
            err_msg = "invalid client_id"
            logger.error(f"{err_msg}", extra={"client_id":client_id})
            return None, err_msg
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
            application = application
        )
        return {
            "user_id" : user.id,
            "access_token" : access_token.token,
            "expires_in_secs" : ACCESS_TOKEN_EXPIRY_IN_SECS,
            "token_type" : "Bearer" 
        }, None
        

    @staticmethod
    def authenticate_client_credentials(base64_encoded_client_credentials = None, client_id = None, client_secret = None):
        # either base64_encoded_client_credentials should be present or client_id and client_secret should be present
        if base64_encoded_client_credentials or (client_id and client_secret):
            if base64_encoded_client_credentials:
                try:
                    decoded_bytes = base64.b64decode(base64_encoded_client_credentials)
                    decoded_str = decoded_bytes.decode('utf-8')
                    client_id, client_secret = decoded_str.split(':', 1)
                except (binascii.Error, ValueError) as e:
                    err_msg = "Invalid base64 encoded client credentials"
                    logger.error(f"{err_msg}: {e}")
                    return None, err_msg
            application = ApplicationDAO.get_application_by_client_id(client_id)
            if not application:
                err_msg = "invalid client_id"
                logger.error(f"{err_msg}", extra={"client_id":client_id})
                return None, err_msg
            # client_secret is stored in the database in hashed format, so we cannot verify the client_secret directly. Instead, we can use the check_client_secret method of the Application model to verify the client_secret.
            if not check_password(client_secret, application.client_secret):
                err_msg = "invalid client_secret"
                logger.error(f"{err_msg}", extra={"client_id":client_id})
                return None, err_msg
            token = random_token_generator(size = ACCESS_TOKEN_SIZE)
            access_token = AccessTokenDAO.create_access_token(
                token=token,
                expiry=datetime.now() + timedelta(seconds=ACCESS_TOKEN_EXPIRY_IN_SECS),
                user = None,
                application = application
            )
            return {
                "access_token" : access_token.token,
                "expires_in_secs" : ACCESS_TOKEN_EXPIRY_IN_SECS,
                "token_type" : "Bearer" 
            }, None

        else:
            err_msg = "either base64_encoded_client_credentials or client_id and client_secret should be present"
            logger.error(err_msg)
            return None, err_msg