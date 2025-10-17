from .core_model import BaseModel
from .user import User
from .place import Place
from typing import Optional
from datetime import datetime
import uuid

class Review(BaseModel):
    def __init__(self, text, rating, user_id, place_id):
        super().__init__()
        self.id = id or str(uuid.uuid4())
        self.text = text
        self.rating = rating
        self.user_id = user_id
        self.place_id = place_id

        # Dates de création et mise à jour
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

        # Validation simple
        if not self.text or not isinstance(self.text, str):
            raise ValueError("Text must be a non-empty string")
        if not isinstance(self.rating, int) or not (1 <= self.rating <= 5):
            raise ValueError("Rating must be an integer between 1 and 5")

    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "rating": self.rating,
            "user_id": getattr(self.user, "id", None),
            "place_id": getattr(self.place, "id", None),
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
