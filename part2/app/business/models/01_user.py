from core_model import BaseModel
from datetime import datetime
from email_validator import validate_email, EmailNotValidError


class User(BaseModel):
    def __init__(self, first_name, last_name, email, password, is_admin):
        super().__init__()
        # self.__user_id = str(uuid.uuid4())
        self.first_name = first_name
        self.last_name = last_name
        self.__email = self._validate_and_set_email(email)
        #self.__password = password BONUS à revoir
        self.__is_admin = is_admin
        # self.__created_at = datetime.now()
        # self.__updated_at = datetime.now()


    #########################################
    ###          GETTER / SETTER          ###
    #########################################
    """ GETTER/SETTER Id """
    @property
    def get_user_id(self, user_id):
        return self.__user_id

    @set_id.setter
    def set_user_id(self, value):
        return self.__user_id = value

    """ GETTER/SETTER Email """
    @property
    def get_email(self, email):
        return self.__email

    @set_email.setter
    def set_email(self, value):
        return self.__email = value

    """ GETTER/SETTER Password """
    @property
    def get_password(self, password):
        return self.__password

    @set_email.setter
    def set_email(self, value):
        return self.__email = value

    """ GETTER/SETTER is_admin """
    @property
    def get_is_admin(self, is_admin):
        return self.__is_admin

    @set_is_admin.setter
    def set_is_admin(self, value):
        return self.__is_admin = value

    """ GETTER/SETTER created_at """
    @property
    def get_created_at(self, created_at):
        return self.__created_at

    @set_email.setter
    def set_created_at(self, value):
        return self.__created_at = value

    """ GETTER/SETTER updated_at """
    @property
    def get_updated_at(self, updated_at):
        return self.__updated_at

    @set_email.setter
    def set_updated_at(self, value):
        return self.__updated_at = value
