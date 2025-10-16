from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('users', description='User operations')

# Model for input validation and Swagger documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user')
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_model)
    @api.response(201, "User successfully created")
    @api.response(400, "Invalid input data")
    def post(self):
        """Create a new user"""
        user_data = api.payload

    # ✅ Vérification des champs requis
        required_fields = ["first_name", "last_name", "email"]
        for field in required_fields:
            value = user_data.get(field, "").strip()
            if not value:
                return {"error": f"{field.replace('_', ' ').capitalize()} is required"}, 400

    # ✅ Vérification email
        import re
        if not re.match(r"[^@]+@[^@]+\.[^@]+", user_data["email"]):
            return {"error": "Invalid email format"}, 400

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
        return [{'id': u.id, 'first_name': u.first_name, 'last_name': u.last_name, 'email': u.email} for u in users], 200

@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email}, 200

    @api.expect(user_model, validate=True)
    @api.response(200, 'User updated successfully')
    @api.response(404, 'User not found')
    def put(self, user_id):
        """Update user details"""
        user_data = api.payload
        updated = facade.update_user(user_id, user_data)
        if not updated:
            return {'error': 'User not found'}, 404
        user = facade.get_user(user_id)
        return {'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email}, 200

    @api.response(200, 'User deleted successfully')
    @api.response(404, 'User not found')
    def delete(self, user_id):
        """Delete a user"""
        deleted = facade.delete_user(user_id)
        if not deleted:
            return {'error': 'User not found'}, 404
        return {'message': 'User deleted'}, 200

