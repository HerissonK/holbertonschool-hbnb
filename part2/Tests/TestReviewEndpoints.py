"""
Tests unitaires pour les avis
"""
import unittest
from app import create_app


class TestReviewEndpoints(unittest.TestCase):
    """Tests pour les endpoints Review"""

    def setUp(self):
        """Configuration avant chaque test"""
        self.app = create_app()
        self.client = self.app.test_client()
        
        # Créer un utilisateur
        user_response = self.client.post('/api/v1/users/', json={
            "first_name": "Reviewer",
            "last_name": "Test",
            "email": "reviewer@example.com"
        })
        self.user_id = user_response.get_json()['id']
        
        # Créer un owner
        owner_response = self.client.post('/api/v1/users/', json={
            "first_name": "Owner",
            "last_name": "Test",
            "email": "owner2@example.com"
        })
        self.owner_id = owner_response.get_json()['id']
        
        # Créer un place
        place_response = self.client.post('/api/v1/places/', json={
            "title": "Test Place",
            "description": "A place to review",
            "price": 100.0,
            "latitude": 45.5,
            "longitude": -73.6,
            "owner_id": self.owner_id
        })
        self.place_id = place_response.get_json()['id']

    def test_create_review_success(self):
        """Test: Création d'une review valide"""
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Great place to stay!",
            "rating": 5,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn('id', data)
        self.assertEqual(data['rating'], 5)

    def test_create_review_empty_text(self):
        """Test: Création avec texte vide"""
        response = self.client.post('/api/v1/reviews/', json={
            "text": "",
            "rating": 5,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        self.assertEqual(response.status_code, 400)

    def test_create_review_invalid_user_id(self):
        """Test: Création avec user_id invalide"""
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Great place!",
            "rating": 5,
            "user_id": "nonexistent-user-id",
            "place_id": self.place_id
        })
        self.assertEqual(response.status_code, 400)

    def test_create_review_invalid_place_id(self):
        """Test: Création avec place_id invalide"""
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Great place!",
            "rating": 5,
            "user_id": self.user_id,
            "place_id": "nonexistent-place-id"
        })
        self.assertEqual(response.status_code, 400)

    def test_create_review_rating_too_high(self):
        """Test: Création avec rating > 5"""
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Amazing!",
            "rating": 6,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        self.assertEqual(response.status_code, 400)

    def test_create_review_rating_too_low(self):
        """Test: Création avec rating < 1"""
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Terrible!",
            "rating": 0,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        self.assertEqual(response.status_code, 400)
