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
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hbnb.db'  # Exemple : SQLite, modifie selon ton usage
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Clé secrète utilisée pour signer les JWT (et sécuriser Flask)
    app.config['SECRET_KEY'] = 'super-secret-key'  # 🔒 À remplacer par une vraie clé en prod
    app.config['JWT_SECRET_KEY'] = app.config['SECRET_KEY']

    # Initialiser SQLAlchemy avec l'app
    jwt.init_app(app)
    db.init_app(app)
    bcrypt.init_app(app)
    # Créer l'API REST
    api = Api(app, version='1.0', title='HBnB API',
              description='HBnB Application API', doc='/api/v1/')

    # Importer les namespaces ici pour éviter les imports circulaires
    from app.API.v1.users import api as users_ns
    from app.API.v1.place import api as places_ns
    from app.API.v1.amenity import api as amenities_ns
    from app.API.v1.review import api as reviews_ns
    from app.API.v1.auth import api as auth_ns

    # Ajouter les namespaces à l'API
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(auth_ns, path='/api/v1/auth')

    return app
