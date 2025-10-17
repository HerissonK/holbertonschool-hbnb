from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('users', description='User operations')

# Model for input validation and Swagger documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'is_admin': fields.Boolean(description='User admin status (default: false)')
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_model)
    @api.response(201, "User successfully created")
    @api.response(400, "Invalid input data")
    def post(self):
        """Create a new user"""
        user_data = api.payload
        user = User(**user_data)

        # ✅ Validation via le modèle
        errors = user.validate()
        if errors:
            return {"errors": errors}, 400

        new_user = facade.create_user(user_data)
        return new_user.to_dict(), 201

    @api.response(200, 'List of users retrieved successfully')
    def get(self):
        """List all users"""
        users = facade.list_users()
        return [u.to_dict() for u in users], 200


@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return user.to_dict(), 200

    @api.expect(user_model)
    @api.response(200, 'User updated successfully')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    def put(self, user_id):
        """Update user details"""
        user_data = api.payload
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        user.update(user_data)
        errors = user.validate()
        if errors:
            return {"errors": errors}, 400

        updated_user = facade.update_user(user_id, user_data)
        return updated_user.to_dict(), 200

    @api.response(200, 'User deleted successfully')
    @api.response(404, 'User not found')
    def delete(self, user_id):
        """Delete a user"""
        deleted = facade.delete_user(user_id)
        if not deleted:
            return {'error': 'User not found'}, 404
        return {'message': 'User deleted'}, 200
