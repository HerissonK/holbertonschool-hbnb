"""
Couche Présentation - API REST
Dépend de la couche Services
Ne doit PAS dépendre directement de Persistance ou Modèle
"""
"""
Couche Présentation - API REST
Dépend de la couche Services
Ne doit PAS dépendre directement de Persistance ou Modèle
"""
from flask import Blueprint
from flask_restx import Api

from app.API.v1.user import api as user_ns
from app.API.v1.place import api as place_ns
from app.API.v1.review import api as review_ns
from app.API.v1.amenity import api as amenity_ns

api_v1 = Blueprint('api_v1', __name__, url_prefix='/api/v1')
api = Api(api_v1, title='HBNB API', version='1.0', description='HBNB REST API')

# Enregistrement des namespaces
api.add_namespace(user_ns)
api.add_namespace(place_ns)
api.add_namespace(review_ns)
api.add_namespace(amenity_ns)

