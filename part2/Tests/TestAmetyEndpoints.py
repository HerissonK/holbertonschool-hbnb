"""
Tests unitaires pour l'API HBnB
"""
import unittest
from app import create_app


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