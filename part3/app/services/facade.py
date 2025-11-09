from app.persistence.SQLAlchemyRepository import SQLAlchemyRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review
from app.models.place_amenity import PlaceAmenity
from app import db

class HBnBFacade:
    def __init__(self):
        self.user_repo = SQLAlchemyRepository(User)  # Switched to SQLAlchemyRepository
        self.place_repo = SQLAlchemyRepository(Place)
        self.review_repo = SQLAlchemyRepository(Review)
        self.amenity_repo = SQLAlchemyRepository(Amenity)

    # Users
    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user
    def get_user(self, user_id):
        return self.user_repo.get(user_id)
    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)
    def list_users(self):
        return self.user_repo.get_all()
    def update_user(self, user_id, data):
        user = self.get_user(user_id)
        if not user:
            return None
        user.update(data)
        db.session.commit()
        return user
    def delete_user(self, user_id):
        return self.user_repo.delete(user_id)

    #Amenity
    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)        
        return amenity
    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)
    def list_amenities(self):
        return self.amenity_repo.get_all()
    def update_amenity(self, amenity_id, data):
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None
        for key, value in data.items():
            setattr(amenity, key, value)
        self.amenity_repo.update(amenity_id, data)  # ✅ correction ici
        return amenity
    def delete_amenity(self, amenity_id):
        return self.amenity_repo.delete(amenity_id)

    # R E V I E W S 
    def create_review(self, review_data):
    # Placeholder for logic to create a review, including validation for user_id, place_id, and rating
        
        new_review = Review(
            text=review_data['text'],
            rating=review_data['rating'],
            place_id=review_data['place_id'],
            user_id=review_data['user_id'] 
        )

        self.review_repo.add(new_review)

        return new_review

    def get_review(self, review_id):
    # Placeholder for logic to retrieve a review by ID
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
    # Placeholder for logic to retrieve all reviews
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
    # Placeholder for logic to retrieve all reviews for a specific place
        all_reviews = self.review_repo.get_all()
        return [review for review in all_reviews if review.place_id == place_id]

    def update_review(self, review_id, review_data):
    # Placeholder for logic to update a review
        review = self.review_repo.get(review_id)
        if not review:
            return None  
        # Mettre à jour les champs autorisés
        allowed_fields = ["text", "rating"]
        for field in allowed_fields:
            if field in review_data:
                setattr(review, field, review_data[field])

        # Sauvegarder dans la DB
        self.review_repo.add(review)
        return review

    def delete_review(self, review_id):
    # Placeholder for logic to delete a review
        return self.review_repo.delete(review_id)

    def get_review_by_user_and_place(self, user_id, place_id):
        """Return the review written by this user for a given place, if any."""
        return self.review_repo.get_by_user_and_place(user_id, place_id)


# Places
    def create_place(self, place_data):
        # Associer le user
        if "user_id" not in place_data or not place_data["user_id"]:
            place_data["user_id"] = place_data["owner_id"]

        amenities_ids = place_data.pop("amenities", [])
        place = Place(**place_data)
        self.place_repo.add(place)

        # Créer les liens PlaceAmenity
        for amenity_id in amenities_ids:
            amenity = self.amenity_repo.get(amenity_id)
            if amenity:
                pa = PlaceAmenity(place_id=place.id, amenity_id=amenity.id)
                db.session.add(pa)
        db.session.commit()
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, data):
        place = self.get_place(place_id)
        if not place:
            return None
        for key, value in data.items():
            setattr(place, key, value)
        db.session.commit()
        return place
