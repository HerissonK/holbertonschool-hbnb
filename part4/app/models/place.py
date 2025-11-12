from app import db
import uuid
from app.models.place_amenity import PlaceAmenity

class Place(db.Model):
    
    __tablename__ = "places"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(128), nullable=False)
    price = db.Column(db.Float(128), nullable=False)
    latitude = db.Column(db.Float(128), nullable=False)
    longitude = db.Column(db.Float(128), nullable=False)
    owner_id = db.Column(db.String(128), nullable=False)
    user_id = db.Column(db.String(128), nullable=False)

    # One to Many relationship
    place_amenities = db.relationship(
        "PlaceAmenity",
        back_populates="place",
        cascade="all, delete-orphan"
    )

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    @property
    def amenities(self):
        """Retourne la liste des Amenity liées via PlaceAmenity"""
        return [pa.amenity for pa in self.place_amenities]
    
    def add_amenity(self, amenity):
        pa = PlaceAmenity(place=self, amenity=amenity)
        db.session.add(pa)
