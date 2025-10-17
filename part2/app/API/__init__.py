from flask import Flask
from flask_restx import Api
from app.API.v1.users import api as users_ns

def create_app():
    app = Flask(__name__)
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API', doc='/api/v1/docs')

    # Register the users namespace
    from app.API.v1.users import api as users_ns
    from app.API.v1.place import api as places_ns
    from app.API.v1.review import api as reviews_ns
    from app.API.v1.amenity import api as amenities_ns

    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(places_ns, path='/api/v1/place')
    api.add_namespace(reviews_ns, path='/api/v1/review')
    api.add_namespace(amenities_ns, path='/api/v1/amenity')

    return app
