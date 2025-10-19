from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review



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
    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
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
    # Vérification existence user
        user = self.get_user(review_data['user_id'])
        if not user:
            raise ValueError("Invalid user_id")

    # Vérification existence place
        place = self.get_place(review_data['place_id'])
        if not place:
            raise ValueError("Invalid place_id")

        new_review = Review(
            text=review_data['text'],
            rating=review_data['rating'],
            user_id=review_data['user_id'],
            place_id=review_data['place_id']
        )

        # Ajouter la review à la place
        place.add_review(new_review)

        # Sauvegarder
        self.review_repo.add(new_review)
        self.place_repo.update(place.id, place.to_dict())  # mettre à jour la place avec la review

        return new_review


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
        return self.review_repo.update(review_id, review_data)

    def delete_review(self, review_id):
    # Placeholder for logic to delete a review
        return self.review_repo.delete(review_id)


# Places
    def create_place(self, place_data):
        owner = self.get_user(place_data.pop("owner_id"))
        place = Place(**place_data)
        self.place_repo.add(place)        
        return place
    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        return self.place_repo.update(place_id, place_data)

facade = HBnBFacade()