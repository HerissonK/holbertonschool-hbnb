#from app import create_app
from flask import Flask
from flask_restx import Api
from app.API.v1.users import api as users_api
from app.API.v1.amenity import api as amenities_api
from app.API.v1.place import api as place_api

app = Flask(__name__)
api = Api(app, version='1.0', title='HBNB API', description='Simple HBNB REST API')

# Enregistrement des namespace
api.add_namespace(users_api, path='/api/v1/users')
api.add_namespace(amenities_api, path='/api/v1/amenities')
api.add_namespace(place_api, path='/api/v1/places')

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
