"""
Tests unitaires pour l'Utilisateur
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
