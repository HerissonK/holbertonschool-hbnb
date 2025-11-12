from app import db  # ton instance SQLAlchemy
import uuid
from app.models.place_amenity import PlaceAmenity

class Amenity(db.Model):

    __tablename__ = "amenities"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(128), nullable=False, unique=True)

    # One to Many relationship
    place_amenities = db.relationship(
        "PlaceAmenity",
        back_populates="amenity",
        cascade="all, delete-orphan"
    )