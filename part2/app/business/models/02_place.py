from core_model import BaseModel
from datetime import datetime

class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner, reviews, amenities):
        super().__init__()
        # self.__place_id = str(uuid.uuid4())
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = user # à verifier
        self.reviews = []  # List to store related reviews
        self.amenities = []  # List to store related amenities

    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)