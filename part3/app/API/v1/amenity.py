from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.facade import HBnBFacade

# Initialisation
api = Namespace('amenity', description='Amenity related operations')
facade = HBnBFacade()

# Schéma de données attendu pour une amenity
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Nom de l\'amenity')
})


@api.route('/')
class AmenityListResource(Resource):
    """Routes pour gérer la liste des amenities"""

    @api.marshal_list_with(amenity_model)
    def get(self):
        """Récupère la liste de toutes les amenities"""
        return facade.list_amenities()

    @jwt_required()
    @api.expect(amenity_model)
    @api.response(201, 'Amenity créée avec succès')
    @api.response(403, 'Accès réservé aux administrateurs')
    def post(self):
        """Crée une nouvelle amenity (admin uniquement)"""
        user_id = get_jwt_identity()
        current_user = facade.user_repo.get(user_id)

        if not current_user or not getattr(current_user, "is_admin", False):
            return {"error": "Admin privileges required"}, 403

        data = request.get_json()
        new_amenity = facade.create_amenity(data)
        return {"message": "Amenity créée avec succès", "id": new_amenity.id}, 201


@api.route('/<string:amenity_id>')
@api.param('amenity_id', 'ID de l\'amenity')
class AmenityResource(Resource):
    """Routes pour gérer une amenity spécifique"""

    @api.marshal_with(amenity_model)
    @api.response(404, 'Amenity introuvable')
    def get(self, amenity_id):
        """Récupère une amenity spécifique"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {"error": "Amenity not found"}, 404
        return amenity

    @jwt_required()
    @api.expect(amenity_model)
    @api.response(200, 'Amenity mise à jour avec succès')
    @api.response(403, 'Accès réservé aux administrateurs')
    @api.response(404, 'Amenity introuvable')
    def put(self, amenity_id):
        """Met à jour une amenity (admin uniquement)"""
        user_id = get_jwt_identity()
        current_user = facade.user_repo.get(user_id)

        if not current_user or not getattr(current_user, "is_admin", False):
            return {"error": "Admin privileges required"}, 403

        data = request.get_json()
        updated = facade.update_amenity(amenity_id, data)

        if not updated:
            return {"error": "Amenity not found"}, 404

        return {"message": "Amenity mise à jour avec succès"}, 200

    @jwt_required()
    @api.response(200, 'Amenity supprimée avec succès')
    @api.response(403, 'Accès réservé aux administrateurs')
    @api.response(404, 'Amenity introuvable')
    def delete(self, amenity_id):
        """Supprime une amenity (admin uniquement)"""
        user_id = get_jwt_identity()
        current_user = facade.user_repo.get(user_id)

        if not current_user or not getattr(current_user, "is_admin", False):
            return {"error": "Admin privileges required"}, 403

        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {"error": "Amenity not found"}, 404

        facade.delete_amenity(amenity_id)
        return {"message": "Amenity supprimée avec succès"}, 200
