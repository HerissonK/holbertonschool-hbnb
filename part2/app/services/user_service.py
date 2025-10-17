"""
Service : UserService
Gère la logique métier liée aux utilisateurs
"""
from app.models.user import User


class UserService:
    @staticmethod
    def create_user(data):
        user = User(
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            email=data.get("email")
        )
        return user
