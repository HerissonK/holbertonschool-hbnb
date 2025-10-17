"""
Tests unitaires pour les lieux
"""
import unittest
from app import create_app


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
