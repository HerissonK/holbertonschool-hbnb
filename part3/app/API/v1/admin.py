from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request
from app.services import facade

api = Namespace("admin", description="Administrator-only operations")

# --- MODELS ---
user_model = api.model("AdminUser", {
    "email": fields.String(required=True, description="User email"),
    "first_name": fields.String(required=True),
    "last_name": fields.String(required=True),
    "password": fields.String(required=True),
    "is_admin": fields.Boolean(description="Admin privileges", default=False)
})

amenity_model = api.model("AdminAmenity", {
    "name": fields.String(required=True, description="Amenity name")
})

# --- ENDPOINTS ---

@api.route("/users/")
class AdminUserCreate(Resource):
    @jwt_required()
    @api.expect(user_model)
    def post(self):
        """Create a new user (Admin only)"""
        current_user = get_jwt_identity()
        if not current_user.get("is_admin"):
            return {"error": "Admin privileges required"}, 403

        data = request.json
        email = data.get("email")

        if facade.get_user_by_email(email):
            return {"error": "Email already registered"}, 400

        new_user = facade.create_user(data)
        return {
            "id": new_user.id,
            "email": new_user.email,
            "is_admin": new_user.is_admin
        }, 201


@api.route("/users/<string:user_id>")
class AdminUserModify(Resource):
    @jwt_required()
    def put(self, user_id):
        """Modify any user's data (Admin only)"""
        current_user = get_jwt_identity()
        if not current_user.get("is_admin"):
            return {"error": "Admin privileges required"}, 403

        data = request.json
        email = data.get("email")

        if email:
            existing_user = facade.get_user_by_email(email)
            if existing_user and existing_user.id != user_id:
                return {"error": "Email already in use"}, 400

        updated_user = facade.update_user(user_id, data)
        if not updated_user:
            return {"error": "User not found"}, 404

        return {"message": "User updated successfully"}, 200


@api.route("/amenities/")
class AdminAmenityCreate(Resource):
    @jwt_required()
    @api.expect(amenity_model)
    def post(self):
        """Create a new amenity (Admin only)"""
        current_user = get_jwt_identity()
        if not current_user.get("is_admin"):
            return {"error": "Admin privileges required"}, 403

        data = request.json
        new_amenity = facade.create_amenity(data)
        return {"id": new_amenity.id, "name": new_amenity.name}, 201


@api.route("/amenities/<string:amenity_id>")
class AdminAmenityModify(Resource):
    @jwt_required()
    @api.expect(amenity_model)
    def put(self, amenity_id):
        """Update an amenity (Admin only)"""
        current_user = get_jwt_identity()
        if not current_user.get("is_admin"):
            return {"error": "Admin privileges required"}, 403

        data = request.json
        updated = facade.update_amenity(amenity_id, data)
        if not updated:
            return {"error": "Amenity not found"}, 404
        return {"message": "Amenity updated successfully"}, 200
