from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

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
    def update_user(self, user_id, user_data):
        return self.user_repo.update(user_id, user_data)
    def delete_user(self, user_id):
        return self.user_repo.delete(user_id)

    #Amenity
    def create_amenity(self, data):
        # Vérifie qu'un nom est fourni
        name = data.get('name')
        if not name:
            raise ValueError("Name is required")
        # Vérifie unicité
        existing = self.amenity_repo.get_by_attribute('name', name)
        if existing:
            return None
        # Crée un objet Amenity (à définir)
        amenity = Amenity(name=name)
        self.amenity_repo.add(amenity)
        return amenity
    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)
    def list_amenities(self):
        return self.amenity_repo.get_all()
    def update_amenity(self, amenity_id, data):
        return self.amenity_repo.update(amenity_id, data)
    def delete_amenity(self, amenity_id):
        return self.amenity_repo.delete(amenity_id)

    # R E V I E W S 
    def create_review(self, review_data):
    # Placeholder for logic to create a review, including validation for user_id, place_id, and rating
        if 'user_id' not in review_data or not review_data['user_id']:
            raise ValueError("Missing user id")

        if 'place_id' not in review_data or not review_data['place_id']:
            raise ValueError("Missing place id")

        if 'rating' not in review_data:
            raise ValueError("Missing rating")

        return self.reviews_repo.post(reviews_id)

    def get_review(self, review_id):
    # Placeholder for logic to retrieve a review by ID
        return self.reviews_repo.get(reviews.id)

    def get_all_reviews(self):
    # Placeholder for logic to retrieve all reviews
        return self.reviews_repo.get(data)

    def get_reviews_by_place(self, place_id):
    # Placeholder for logic to retrieve all reviews for a specific place
        return self.reviews_repo.get(place_id)

    def update_review(self, review_id, review_data):
    # Placeholder for logic to update a review
        return self.reviews_repo.update(reviews_id, review_data)

    def delete_review(self, review_id):
    # Placeholder for logic to delete a review
        return self.reviews_repo.delete(reviews_id)

# Places
    def create_place(self, place_data):
        owner = self.user_repo.get(place_data.get("owner_id"))
        place = Place(
            title=place_data.get("title"),
            description=place_data.get("description"),
            price=place_data.get("price"),
            latitude=place_data.get("latitude"),
            longitude=place_data.get("longitude"),
            owner=owner
        )
        place.amenities = place_data.get("amenities", [])
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        return self.place_repo.update(place_id, place_data)
