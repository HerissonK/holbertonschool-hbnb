from app.models.review import Review
from app.models.user import User
from app.models.place import Place

def test_review_creation():
    # Création d'un utilisateur
    owner = User(first_name="Alice", last_name="Smith", email="alice.smith@example.com")
    
    # Création d'un lieu
    place = Place(
        title="Cozy Apartment",
        description="A nice place to stay",
        price=100,
        latitude=37.7749,
        longitude=-122.4194,
        owner=owner
    )

    # Création d'une review
    review = Review(text="Great stay!", rating=5, user=owner, place=place)

    # Vérifications
    assert review.text == "Great stay!"
    assert review.rating == 5
    assert review.user == owner
    assert review.place == place

    print("Review creation and relationship test passed!")

if __name__ == "__main__":
    test_review_creation()
