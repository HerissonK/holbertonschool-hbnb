class Review(BaseModel):
    def __init__(self, rate, comment, place, date_creation, user):
        super().__init__()
        self.rate = rate
        self.comment = comment
        self.place = place
        self.date_creation = date_creation
        self.user = user

    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)