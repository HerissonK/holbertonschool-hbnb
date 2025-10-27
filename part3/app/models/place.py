from .core_model import BaseModel
from datetime import datetime

class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner_id, reviews=None, amenities=None):
        super().__init__()
        # self.__place_id = str(uuid.uuid4())
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id # à verifier
        self.reviews = reviews if reviews is not None else []
        self.amenities = amenities if amenities is not None else []

    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)