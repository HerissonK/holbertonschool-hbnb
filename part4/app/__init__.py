from flask import Flask
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

# Initialisation
jwt = JWTManager()
bcrypt = Bcrypt()
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hbnb.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'super-secret-key'
    app.config['JWT_SECRET_KEY'] = app.config['SECRET_KEY']

    # Initialisation des extensions
    jwt.init_app(app)
    db.init_app(app)
    bcrypt.init_app(app)

    # Création de l'API principale
    api = Api(app, version='1.0', title='HBnB API',
              description='HBnB Application API', doc='/api/v1/')

    # Import des namespaces RESTX
    from app.API.v1.users import api as users_ns
    from app.API.v1.place import api as places_ns
    from app.API.v1.amenity import api as amenities_ns
    from app.API.v1.review import api as reviews_ns
    from app.API.v1.auth import api as auth_ns
    from app.API.v1.admin import api as admin_ns
    from app.API.v1.debug import api as debug_ns

    # Enregistrement des namespaces
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(auth_ns, path='/api/v1/auth')
    api.add_namespace(admin_ns, path='/api/v1/admin')
    api.add_namespace(debug_ns, path='/api/v1/debug')  # ✅ Ajouté ici

    return app
