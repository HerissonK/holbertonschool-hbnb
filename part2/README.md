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
    api.add_namespace(places_ns, path='/places')
    api.add_namespace(reviews_ns, path='/reviews')
    api.add_namespace(amenities_ns, path='/amenities')

    return app
```

## **Structure complète avec le principe des couches :**
```
app/
├── __init__.py                      # Point d'entrée - Assemblage
│
├── models/                          # COUCHE 1: Entités (pas de dépendances)
│   ├── __init__.py
│   ├── base_model.py
│   ├── user.py
│   ├── place.py
│   ├── review.py
│   └── amenity.py
│
├── persistence/                     # COUCHE 2: Accès données (dépend de models)
│   ├── __init__.py
│   └── repository.py
│
├── services/                        # COUCHE 3: Logique métier (dépend de persistence + models)
│   ├── __init__.py
│   └── facade.py
│
└── API/                             # COUCHE 4: Présentation (dépend de services)
    └── v1/
        ├── __init__.py
        ├── users.py
        ├── places.py
        ├── reviews.py
        └── amenities.py
```

## **Principe des dépendances (IMPORTANT) :**
```
┌─────────────────────────────────────┐
│   API (Présentation)                │  ← Couche 4
│   - Endpoints REST                  │
│   - Validation des entrées          │
└──────────────┬──────────────────────┘
               │ dépend de ↓
┌──────────────▼──────────────────────┐
│   Services (Business Logic)         │  ← Couche 3
│   - Logique métier                  │
│   - Orchestration                   │
└──────────────┬──────────────────────┘
               │ dépend de ↓
┌──────────────▼──────────────────────┐
│   Persistence (Data Access)         │  ← Couche 2
│   - Accès aux données               │
│   - CRUD operations                 │
└──────────────┬──────────────────────┘
               │ dépend de ↓
┌──────────────▼──────────────────────┐
│   Models (Entities)                 │  ← Couche 1
│   - Entités du domaine              │
│   - Pas de dépendances externes     │
└─────────────────────────────────────┘