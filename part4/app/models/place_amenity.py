from app import db  # ton instance SQLAlchemy
import uuid

class PlaceAmenity(db.Model):
    __tablename__ = "place_amenity"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    place_id = db.Column(db.String(36), db.ForeignKey("places.id"), nullable=False)
    amenity_id = db.Column(db.String(36), db.ForeignKey("amenities.id"), nullable=False)

    # One to Many relationship
    place = db.relationship("Place", back_populates="place_amenities")
    amenity = db.relationship("Amenity", back_populates="place_amenities")
