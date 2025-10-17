"""
Point d'entrée principal de l'application
Assemble toutes les couches et configure Flask
"""
from flask import Flask
from app.API import api_v1


def create_app():
    """Factory pattern - crée et configure l’application Flask"""
    app = Flask(__name__)

    # Configuration Flask-RESTX
    app.config['RESTX_MASK_SWAGGER'] = False
    app.config['ERROR_404_HELP'] = False
    app.config['RESTX_VALIDATE'] = True

    # Enregistrer le blueprint principal
    app.register_blueprint(api_v1)

    return app
