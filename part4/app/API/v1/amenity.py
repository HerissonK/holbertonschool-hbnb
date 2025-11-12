from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError
from app import db
from app.services.facade import HBnBFacade

# Namespace pour regrouper les routes liées aux amenities
api = Namespace('amenity', description='Opérations liées aux amenities')
facade = HBnBFacade()

# Modèle de données pour la documentation Swagger
amenity_model = api.model('Amenity', {
    'id': fields.String(readonly=True, description="Identifiant unique de l'amenity"),
    'name': fields.String(required=True, description="Nom de l'amenity")
})


@api.route('/')
class AmenityListResource(Resource):
    """Routes pour gérer la liste complète des amenities"""

    @api.marshal_list_with(amenity_model)
    def get(self):
        """Récupère la liste de toutes les amenities"""
        return facade.list_amenities()

    @jwt_required()
    @api.expect(amenity_model)
    @api.response(201, "Amenity créée avec succès")
    @api.response(400, "Une amenity avec ce nom existe déjà")
    @api.response(403, "Accès réservé aux administrateurs")
    def post(self):
        """Crée une nouvelle amenity (réservé aux admins)"""
        user_id = get_jwt_identity()
        current_user = facade.user_repo.get(user_id)

        if not current_user or not getattr(current_user, "is_admin", False):
            return {"error": "Admin privileges required"}, 403

        data = request.get_json()
        name = data.get("name", "").strip()

        if not name:
            return {"error": "Le champ 'name' est requis"}, 400

        try:
            new_amenity = facade.create_amenity({"name": name})
            return {
                "message": f"Amenity '{name}' créée avec succès",
                "id": new_amenity.id
            }, 201
        except IntegrityError:
            db.session.rollback()
            return {"error": f"L'amenity '{name}' existe déjà"}, 400


@api.route('/<string:amenity_id>')
@api.param('amenity_id', "ID de l'amenity")
class AmenityResource(Resource):
    """Routes pour gérer une amenity spécifique"""

    @api.marshal_with(amenity_model)
    @api.response(404, "Amenity introuvable")
    def get(self, amenity_id):
        """Récupère une amenity spécifique"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {"error": "Amenity not found"}, 404
        return amenity

    @jwt_required()
    @api.response(200, "Amenity supprimée avec succès")
    @api.response(403, "Accès réservé aux administrateurs")
    @api.response(404, "Amenity introuvable")
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
