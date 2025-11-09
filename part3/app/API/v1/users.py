from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade
from app.models.user import User
from app import bcrypt
import re

api = Namespace('users', description='User operations')

user_model = api.model('User', {
    'first_name': fields.String(required=True),
    'last_name': fields.String(required=True),
    'email': fields.String(required=True),
    'password': fields.String(required=True),
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_model)
    @jwt_required()
    def post(self):
        """Create a new user (admin only)"""
        claims = get_jwt()
        if not claims.get("is_admin", False):
            return {"error": "Admin privileges required"}, 403

        user_data = api.payload

        # Vérifications simples
        for field in ["first_name", "last_name", "email", "password"]:
            if not user_data.get(field, "").strip():
                return {"error": f"{field} is required"}, 400

        # Email format
        if not re.match(r"[^@]+@[^@]+\.[^@]+", user_data["email"]):
            return {"error": "Invalid email format"}, 400

        # Email unique
        if facade.get_user_by_email(user_data["email"]):
            return {"error": "Email already in use"}, 400

        # Hash password
        user_data["password"] = user_data["password"]

        new_user = facade.create_user(user_data)

        return {
            "id": new_user.id,
            "first_name": new_user.first_name,
            "last_name": new_user.last_name,
            "email": new_user.email
        }, 201


    @api.response(200, 'List of users retrieved successfully')
    def get(self):
        """List all users"""
        users = facade.list_users()
        print("DEBUG USERS:", [(u.id, u.email) for u in users])

        return [
            {'id': u.id, 'first_name': u.first_name, 'last_name': u.last_name, 'email': u.email}
            for u in users
        ], 200


@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }, 200

    @api.response(200, 'User updated successfully')
    @api.response(404, 'User not found')
    @jwt_required()
    def put(self, user_id):
        """Update user details (admin or the user themselves)"""
        claims = get_jwt()
        current_user_id = get_jwt_identity()
        is_admin = claims.get("is_admin", False)

        # Récupération de l'utilisateur cible
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        # 🔐 Vérification des permissions :
        # - autorisé si admin
        # - ou si l'utilisateur modifie son propre compte
        if not is_admin and str(user.id) != str(current_user_id):
            return {"error": "You are not allowed to modify this user"}, 403

        user_data = api.payload
        if not user_data:
            return {"error": "No data provided"}, 400

        # ✅ Vérifie que les champs requis sont bien fournis
        required_fields = ['first_name', 'last_name', 'email']
        for field in required_fields:
            if field not in user_data or not user_data[field].strip():
                return {"error": f"{field.replace('_', ' ').capitalize()} is required"}, 400

        # ✅ Vérifie unicité de l'email
        existing_user = facade.get_user_by_email(user_data["email"])
        if existing_user and existing_user.id != user.id:
            return {"error": "Email already in use"}, 400

        # ✅ Hash du mot de passe s’il est fourni
        if "password" in user_data and user_data["password"]:
            user_data["password"] = bcrypt.generate_password_hash(user_data["password"]).decode("utf-8")

        updated_user = facade.update_user(user_id, user_data)

        return {
            'id': updated_user.id,
            'first_name': updated_user.first_name,
            'last_name': updated_user.last_name,
            'email': updated_user.email
        }, 200