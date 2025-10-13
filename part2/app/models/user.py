from .core_model import BaseModel
from datetime import datetime
import uuid

class User(BaseModel):
    def __init__(self, first_name, last_name, email, password=None, is_admin=False):
        super().__init__()
        self.__user_id = str(uuid.uuid4())
        self.first_name = first_name
        self.last_name = last_name
        self.__email = email
        self.__password = password
        self.__is_admin = is_admin
        self.__created_at = datetime.now()
        self.__updated_at = datetime.now()

    # user_id
    @property
    def user_id(self):
        return self.__user_id

    @user_id.setter
    def user_id(self, value):
        self.__user_id = value

    # email
    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, value):
        self.__email = value

    # password
    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, value):
        self.__password = value

    # is_admin
    @property
    def is_admin(self):
        return self.__is_admin

    @is_admin.setter
    def is_admin(self, value):
        self.__is_admin = value

    # created_at
    @property
    def created_at(self):
        return self.__created_at

    @created_at.setter
    def created_at(self, value):
        self.__created_at = value

    # updated_at
    @property
    def updated_at(self):
        return self.__updated_at

    @updated_at.setter
    def updated_at(self, value):
        self.__updated_at = value
