#from app import create_app
from flask import Flask
from flask_restx import Api
from app.API.v1.users import api as users_api

app = Flask(__name__)
api = Api(app, version='1.0', title='HBNB API', description='Simple HBNB REST API')

# Enregistrement du namespace
api.add_namespace(users_api, path='/api/v1/users')

if __name__ == '__main__':
    app.run(debug=True)
