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
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn('id', data)
        self.assertEqual(data['name'], 'WiFi')

    def test_create_amenity_empty_name(self):
        """Test: Création avec un nom vide"""
        response = self.client.post('/api/v1/amenities/', json={
            "name": ""
        })
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)

    def test_create_amenity_missing_name(self):
        """Test: Création sans champ 'name'"""
        response = self.client.post('/api/v1/amenities/', json={})
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('errors', data)

    def test_get_amenity_success(self):
        """Test: Récupération d'une amenity existante"""
        # Créer une amenity
        create_resp = self.client.post('/api/v1/amenities/', json={"name": "Pool"})
        amenity_id = create_resp.get_json()['id']

        # Récupérer cette amenity
        response = self.client.get(f'/api/v1/amenities/{amenity_id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['name'], 'Pool')

    def test_get_amenity_not_found(self):
        """Test: Récupération d'une amenity inexistante"""
        response = self.client.get('/api/v1/amenities/nonexistent-id')
        self.assertEqual(response.status_code, 404)

if __name__ == "__main__":
    unittest.main(verbosity=2)
