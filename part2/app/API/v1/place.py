from flask_restx import Namespace, Resource, fields
from app.services import facade
from app.models.place import Place

api = Namespace('places', description='Place operations')

# Models pour Swagger / validation
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

# Model Place pour validation et Swagger
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.String, required=True, description="List of amenities ID's")
})

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new place"""

        place_data = api.payload
        required_fields = ["title", "description", "price", "latitude", "longitude", "owner"]

        for field in required_fields:
            value = place_data.get(field)
        if value is None:
            return {"error": f"{field.replace('_', ' ').capitalize()} is required"}, 400

    # Vérification spécifique pour les champs texte
        if field in ["title", "description", "owner"] and isinstance(value, str):
            if not value.strip():
                return {"error": f"{field.replace('_', ' ').capitalize()} cannot be empty"}, 400

    # Vérification spécifique pour les champs numériques
        if field in ["price", "latitude", "longitude"] and not isinstance(value, (int, float)):
            return {"error": f"{field.replace('_', ' ').capitalize()} must be a number"}, 400

        place = Place(
            title=place_data["title"],
            description=place_data["description"],
            price=place_data["price"],
            latitude=place_data["latitude"],
            longitude=place_data["longitude"],
            owner=place_data["owner"],
            amenities=place_data.get("amenities", [])
            )
        
        return {
            "id": place.id,
            "title": place.title,
            "description": place.description,
            "price": place.price,
            "latitude": place.latitude,
            "longitude": place.longitude,
            "owner_id": place.owner, 
            "amenities": place.amenities,
            "created_at": place.created_at.isoformat()
            }, 201


    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        places = facade.get_all_places()
        result = []
        for place in places:
            result.append({
                'id': place.id,
                'title': place.title,
                'description': place.description,
                'price': place.price,
                'latitude': place.latitude,
                'longitude': place.longitude,
                'owner_id': getattr(place.owner, 'id', place.owner),  # si owner est juste un ID
                'amenities': getattr(place, 'amenities', [])          # renvoie directement la liste de str
            })
        return result, 200


@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        return {
            "id": place.id,
            "title": getattr(place, "title", ""),
            "description": getattr(place, "description", ""),
            "price": getattr(place, "price", 0.0),
            "latitude": getattr(place, "latitude", 0.0),
            "longitude": getattr(place, "longitude", 0.0),
            "owner_id": getattr(place.owner, 'id', place.owner),  # renvoyer l'id
            "amenities": getattr(place, "amenities", []),
            "created_at": getattr(place, "created_at", None).isoformat() if getattr(place, "created_at", None) else None,
            "updated_at": getattr(place, "updated_at", None).isoformat() if getattr(place, "updated_at", None) else None
        }, 200

    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update a place's information"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        updated_place = facade.place_repo.update(place_id, api.payload)
        if not updated_place:
            return {'error': 'Failed to update place'}, 400

    # Verification du remplissage de la totalite des champs
        required_fields = ['id', 'name']
        for field in required_fields:
            if field not in place or place[field] in ("", None):
                return {"error": f"{field.replace('_', ' ').capitalize()} is required"}, 400

    # Verification spécifique pour le contenue de la description
        description = data_review.get('description')
        if description in ("", None):
            return {"error": "description is required"}, 400

        if not isinstance(description, str):
            return {"error": "The description should a text"}, 400

        return {
            'id': updated_place.id,
            'title': updated_place.title,
            'description': updated_place.description,
            'price': updated_place.price,
            'latitude': updated_place.latitude,
            'longitude': updated_place.longitude,
            'owner_id': getattr(updated_place.owner, 'id', updated_place.owner),
            'amenities': getattr(updated_place, 'amenities', []),
            'updated_at': updated_place.updated_at.isoformat()
        }, 200
