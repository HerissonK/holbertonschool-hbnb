from .core_model import BaseModel
from datetime import datetime
import uuid

class Review(BaseModel):
    def __init__(self, text: str, rating: int, user_id: str, place_id: str,
                 id: str = None, created_at: datetime = None, updated_at: datetime = None):
        super().__init__()
        self.id = id or str(uuid.uuid4())
        self.text = text
        self.rating = rating
        self.user_id = user_id
        self.place_id = place_id
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()

        # Validation simple
        if not self.text or not isinstance(self.text, str):
            raise ValueError("Text must be a non-empty string")
        if not isinstance(self.rating, int) or not (1 <= self.rating <= 5):
            raise ValueError("Rating must be an integer between 1 and 5")
        if not self.user_id or not isinstance(self.user_id, str):
            raise ValueError("user_id must be a non-empty string")
        if not self.place_id or not isinstance(self.place_id, str):
            raise ValueError("place_id must be a non-empty string")

    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "rating": self.rating,
            "user_id": self.user_id,
            "place_id": self.place_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
