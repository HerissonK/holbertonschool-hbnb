from .core_model import BaseModel
import uuid
import re
from typing import Optional

class User(BaseModel):
    def __init__(self, first_name, last_name, email, is_admin=False, id=None):
        super().__init__()
        self.id = id or str(uuid.uuid4())
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin  # ✅ nouvel attribut booléen par défaut à False

    # ✅ Validation des données utilisateur
    def validate(self):
        """Vérifie que les données utilisateur sont valides."""
        errors = {}

        if not self.first_name or not self.first_name.strip():
            errors["first_name"] = "First name is required"
        if not self.last_name or not self.last_name.strip():
            errors["last_name"] = "Last name is required"
        if not self.email or not self.email.strip():
            errors["email"] = "Email is required"
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", self.email):
            errors["email"] = "Invalid email format"

        return errors

    # ✅ Mise à jour des champs
    def update(self, data):
        for key, value in data.items():
            if key not in ["id", "created_at"]:
                setattr(self, key, value)

    # ✅ Conversion en dictionnaire
    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "is_admin": self.is_admin,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
