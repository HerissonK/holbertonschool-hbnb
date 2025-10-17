from .core_model import BaseModel
from datetime import datetime
from typing import List, Optional, TYPE_CHECKING
from .user import User
from .review import Review
import uuid

# Imports uniquement pour le type checking (pas au runtime)
if TYPE_CHECKING:
    from .user import User
    from .review import Review

class Place(BaseModel):
    def __init__(
        self,
        title: str,
        description: str,
        price: float,
        latitude: float,
        longitude: float,
        owner: Optional[User] = None,
        reviews: Optional[List[Review]] = None,
        amenities: Optional[List[str]] = None,
        id: Optional[str] = None
    ):
        super().__init__()
        self.id = id or str(uuid.uuid4())
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.reviews = reviews if reviews is not None else []
        self.amenities = amenities if amenities is not None else []

    def add_review(self, review: Review):
        """Add a review to the place."""
        self.reviews.append(review)

    def add_amenity(self, amenity: str):
        """Add an amenity to the place."""
        self.amenities.append(amenity)

    def to_dict(self):
        """Serialize the Place to a dictionary."""
        owner_data = None
        if self.owner is not None:
            owner_data = {
                "id": getattr(self.owner, "id", None),
                "first_name": getattr(self.owner, "first_name", None),
                "last_name": getattr(self.owner, "last_name", None),
                "email": getattr(self.owner, "email", None),
            }

        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner": owner_data,
            "reviews": [r.to_dict() for r in self.reviews],
            "amenities": self.amenities,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
