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

        # Récupérer l'utilisateur quel que soit son rôle
        user = facade.get_user_by_email(email)

        # Vérifie que l'utilisateur existe et que le mot de passe est correct
        if not user or not user.verify_password(password):
            return {'error': 'Invalid credentials'}, 401

        # Génère un JWT pour tout utilisateur (admin ou non)
        access_token = create_access_token(
            identity=user.id,  # doit être un int ou string
            additional_claims={
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
         print("jwt------")
         print(get_jwt_identity())
         current_user = get_jwt_identity() # Retrieve the user's identity from the token
         #if you need to see if the user is an admin or not, you can access additional claims using get_jwt() :
         # addtional claims = get_jwt()
         #additional claims["is_admin"] -> True or False
         return {'message': f'Hello, user {current_user}'}, 200