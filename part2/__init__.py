"""
Point d'entrée de l'application
Configure et assemble toutes les couches
"""
from flask import Flask
from flask_restx import Api


def create_app(config_name=None):
    """
    Factory pattern pour créer l'application Flask
    
    Args:
        config_name: Nom de la configuration (development, production, testing)
    
    Returns:
        app: Instance Flask configurée
    """
    app = Flask(__name__)
    
    # Configuration de l'application
    app.config['RESTX_MASK_SWAGGER'] = False
    app.config['ERROR_404_HELP'] = False
    app.config['RESTX_VALIDATE'] = True
    
    # Créer l'API avec documentation Swagger
    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='HBnB Application API - Architecture en couches',
        doc='/api/v1/docs',
        prefix='/api/v1'
    )

    # Enregistrer les namespaces (Couche Présentation)
    # Import ici pour éviter les imports circulaires
    from app.API.v1.users import api as users_ns
    from app.API.v1.places import api as places_ns
    from app.API.v1.reviews import api as reviews_ns
    from app.API.v1.amenities import api as amenities_ns

    # Ajouter les namespaces avec leurs chemins
    api.add_namespace(users_ns, path='/users')
    api.add_namespace(places_ns, path='/place')
    api.add_namespace(reviews_ns, path='/review')
    api.add_namespace(amenities_ns, path='/amenity')

    return app
