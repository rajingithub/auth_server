from abc import ABC, abstractmethod
from accounts.dao.user_dao import UserDAO
from utils.logger import logger

class IAuthBackend(ABC):
    @abstractmethod
    def authenticate(user_identifier, password):
        pass


class UsernameAuthBackend(IAuthBackend):
    @staticmethod
    def authenticate(user_identifier, password):
        user = UserDAO.get_user_by_username(username=user_identifier)
        if not user:
            err_msg = "username not present"
            logger.error(f"{err_msg}", extra={"username":user_identifier})
            return None, err_msg
        if not user.check_password(raw_password=password):
            err_msg = "invalid password"
            logger.error(f"{err_msg}", extra={"username":user_identifier})
            return None, None
        logger.info("user is authenicated with username and password", extra={"username":user_identifier, "user_id":user.id})
        return user, None
    

class EmailAuthBackend(IAuthBackend):
    @staticmethod
    def authenticate(user_identifier, password):
        users = UserDAO.get_users_by_email(email=user_identifier)
        if not users:
            err_msg = "email not present"
            logger.error(f"{err_msg}", extra={"email":user_identifier})
            return None, err_msg
        if len(users)>1:
            err_msg = "multiple users found with same email"
            logger.error(f"{err_msg}", extra={"email":user_identifier})
            return None, err_msg
        user = users[0]
        if not user.check_password(raw_password=password):
            err_msg = "invalid password"
            logger.error(f"{err_msg}", extra={"email":user_identifier})
            return None, None
        logger.info("user is authenicated with username and password", extra={"username":user_identifier, "user_id":user.id})
        return user, None 
            
