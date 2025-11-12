from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.services import facade

api = Namespace('auth', description='Authentication operations')

login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

@api.route('/login')
class Login(Resource):
    @api.expect(login_model)
    def post(self):
        """Authenticate user and return a JWT token for any user"""
        credentials = api.payload
        email = credentials.get('email')
        password = credentials.get('password')

        if not email or not password:
            return {'error': 'Email and password are required'}, 400

        user = facade.get_user_by_email(email)

        if not user or not user.verify_password(password):
            return {'error': 'Invalid credentials'}, 401

        access_token = create_access_token(
            identity=user.id,
            additional_claims={
                "id": user.id,
                "email": user.email,
                "is_admin": user.is_admin
            }
        )

        return {'access_token': access_token}, 200


@api.route('/protected')
class ProtectedResource(Resource):
    @jwt_required()
    def get(self):
        """A protected endpoint that requires a valid JWT token"""
        current_user = get_jwt_identity()
        return {'message': f'Hello, user {current_user}'}, 200
