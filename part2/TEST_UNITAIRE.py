"""
Tests unitaires pour l'API HBnB
"""
import unittest
from app import create_app


class TestUserEndpoints(unittest.TestCase):
    """Tests pour les endpoints User"""

    def setUp(self):
        """Configuration avant chaque test"""
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_user_success(self):
        """Test: Création d'un utilisateur valide"""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com"
        })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn('id', data)
        self.assertEqual(data['first_name'], 'Jane')

    def test_create_user_empty_firstname(self):
        """Test: Création avec first_name vide"""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "",
            "last_name": "Doe",
            "email": "test@example.com"
        })
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)

    def test_create_user_empty_lastname(self):
        """Test: Création avec last_name vide"""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "",
            "email": "test@example.com"
        })
        self.assertEqual(response.status_code, 400)

    def test_create_user_invalid_email(self):
        """Test: Création avec email invalide"""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "invalid-email"
        })
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)

    def test_create_user_empty_email(self):
        """Test: Création avec email vide"""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": ""
        })
        self.assertEqual(response.status_code, 400)

    def test_get_user_success(self):
        """Test: Récupération d'un utilisateur existant"""
        # Créer d'abord un utilisateur
        create_response = self.client.post('/api/v1/users/', json={
            "first_name": "Test",
            "last_name": "User",
            "email": "test@example.com"
        })
        user_id = create_response.get_json()['id']
        
        # Récupérer l'utilisateur
        response = self.client.get(f'/api/v1/users/{user_id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['email'], 'test@example.com')

    def test_get_user_not_found(self):
        """Test: Récupération d'un utilisateur inexistant"""
        response = self.client.get('/api/v1/users/nonexistent-id')
        self.assertEqual(response.status_code, 404)


class TestPlaceEndpoints(unittest.TestCase):
    """Tests pour les endpoints Place"""

    def setUp(self):
        """Configuration avant chaque test"""
        self.app = create_app()
        self.client = self.app.test_client()
        
        # Créer un utilisateur pour les tests
        user_response = self.client.post('/api/v1/users/', json={
            "first_name": "Owner",
            "last_name": "Test",
            "email": "owner@example.com"
        })
        self.owner_id = user_response.get_json()['id']

    def test_create_place_success(self):
        """Test: Création d'un place valide"""
        response = self.client.post('/api/v1/places/', json={
            "title": "Beautiful Apartment",
            "description": "A nice place to stay",
            "price": 100.0,
            "latitude": 45.5,
            "longitude": -73.6,
            "owner_id": self.owner_id
        })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn('id', data)
        self.assertEqual(data['title'], 'Beautiful Apartment')

    def test_create_place_empty_title(self):
        """Test: Création avec titre vide"""
        response = self.client.post('/api/v1/places/', json={
            "title": "",
            "description": "A nice place",
            "price": 100.0,
            "latitude": 45.5,
            "longitude": -73.6,
            "owner_id": self.owner_id
        })
        self.assertEqual(response.status_code, 400)

    def test_create_place_negative_price(self):
        """Test: Création avec prix négatif"""
        response = self.client.post('/api/v1/places/', json={
            "title": "Test Place",
            "description": "A nice place",
            "price": -50.0,
            "latitude": 45.5,
            "longitude": -73.6,
            "owner_id": self.owner_id
        })
        self.assertEqual(response.status_code, 400)

    def test_create_place_zero_price(self):
        """Test: Création avec prix à zéro"""
        response = self.client.post('/api/v1/places/', json={
            "title": "Test Place",
            "description": "A nice place",
            "price": 0,
            "latitude": 45.5,
            "longitude": -73.6,
            "owner_id": self.owner_id
        })
        self.assertEqual(response.status_code, 400)

    def test_create_place_invalid_latitude_high(self):
        """Test: Création avec latitude > 90"""
        response = self.client.post('/api/v1/places/', json={
            "title": "Test Place",
            "description": "A nice place",
            "price": 100.0,
            "latitude": 95.0,
            "longitude": -73.6,
            "owner_id": self.owner_id
        })
        self.assertEqual(response.status_code, 400)

    def test_create_place_invalid_latitude_low(self):
        """Test: Création avec latitude < -90"""
        response = self.client.post('/api/v1/places/', json={
            "title": "Test Place",
            "description": "A nice place",
            "price": 100.0,
            "latitude": -95.0,
            "longitude": -73.6,
            "owner_id": self.owner_id
        })
        self.assertEqual(response.status_code, 400)

    def test_create_place_invalid_longitude_high(self):
        """Test: Création avec longitude > 180"""
        response = self.client.post('/api/v1/places/', json={
            "title": "Test Place",
            "description": "A nice place",
            "price": 100.0,
            "latitude": 45.5,
            "longitude": 190.0,
            "owner_id": self.owner_id
        })
        self.assertEqual(response.status_code, 400)

    def test_create_place_invalid_longitude_low(self):
        """Test: Création avec longitude < -180"""
        response = self.client.post('/api/v1/places/', json={
            "title": "Test Place",
            "description": "A nice place",
            "price": 100.0,
            "latitude": 45.5,
            "longitude": -190.0,
            "owner_id": self.owner_id
        })
        self.assertEqual(response.status_code, 400)

    def test_create_place_boundary_latitude_valid(self):
        """Test: Création avec latitude aux limites valides"""
        # Test latitude = 90
        response = self.client.post('/api/v1/places/', json={
            "title": "North Pole",
            "description": "At the top",
            "price": 100.0,
            "latitude": 90.0,
            "longitude": 0.0,
            "owner_id": self.owner_id
        })
        self.assertEqual(response.status_code, 201)
        
        # Test latitude = -90
        response = self.client.post('/api/v1/places/', json={
            "title": "South Pole",
            "description": "At the bottom",
            "price": 100.0,
            "latitude": -90.0,
            "longitude": 0.0,
            "owner_id": self.owner_id
        })
        self.assertEqual(response.status_code, 201)

    def test_create_place_boundary_longitude_valid(self):
        """Test: Création avec longitude aux limites valides"""
        # Test longitude = 180
        response = self.client.post('/api/v1/places/', json={
            "title": "East Edge",
            "description": "Far east",
            "price": 100.0,
            "latitude": 0.0,
            "longitude": 180.0,
            "owner_id": self.owner_id
        })
        self.assertEqual(response.status_code, 201)
        
        # Test longitude = -180
        response = self.client.post('/api/v1/places/', json={
            "title": "West Edge",
            "description": "Far west",
            "price": 100.0,
            "latitude": 0.0,
            "longitude": -180.0,
            "owner_id": self.owner_id
        })
        self.assertEqual(response.status_code, 201)


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


class TestAmenityEndpoints(unittest.TestCase):
    """Tests pour les endpoints Amenity"""

    def setUp(self):
        """Configuration avant chaque test"""
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_amenity_success(self):
        """Test: Création d'une amenity valide"""
        response = self.client.post('/api/v1/amenities/', json={
            "name": "WiFi"
        })