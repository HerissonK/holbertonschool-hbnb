from flask_restx import Namespace, Resource, fields
from app.services import facade

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
    # ✅ on accepte aussi user_id pour compatibilité
    'owner_id': fields.String(description='ID of the owner'),
    'user_id': fields.String(description='Alternative ID of the owner (user)'),
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

        # ✅ Vérification des champs requis
        required_fields = ["title", "price", "latitude", "longitude"]
        for field in required_fields:
            value = place_data.get(field)
            if value is None or (isinstance(value, str) and not value.strip()):
                return {"error": f"{field.replace('_', ' ').capitalize()} is required"}, 400

        # ✅ Vérification du prix
        if not isinstance(place_data["price"], (int, float)):
            return {"error": "Price must be a number"}, 400
        if place_data["price"] < 0:
            return {"error": "Price cannot be negative"}, 400

        # ✅ Vérification latitude / longitude
        lat = place_data["latitude"]
        lon = place_data["longitude"]
        if not isinstance(lat, (int, float)) or not isinstance(lon, (int, float)):
            return {"error": "Latitude and longitude must be numbers"}, 400

        # ✅ Vérification des valeurs valides
        if not -90 <= lat <= 90:
            return {"error": "Latitude must be between -90 and 90"}, 400
        if not -180 <= lon <= 180:
            return {"error": "Longitude must be between -180 and 180"}, 400

        # ✅ Vérification du propriétaire (user_id ou owner_id)
        owner_id = place_data.get("owner_id") or place_data.get("user_id")
        if not owner_id:
            return {"error": "Owner ID (owner_id or user_id) is required"}, 400

        owner = facade.get_user(owner_id)
        if not owner:
            return {"error": "Owner ID does not exist"}, 400

        # ✅ Vérification des amenities (existence)
        amenities_ids = place_data.get("amenities", [])
        if not isinstance(amenities_ids, list):
            return {"error": "Amenities must be a list"}, 400

        # Vérifier que chaque amenity existe
        for amenity_id in amenities_ids:
            amenity = facade.get_amenity(amenity_id)
            if not amenity:
                return {"error": f"Amenity with ID {amenity_id} does not exist"}, 400

        # ✅ Création du lieu
        place_data["owner_id"] = owner_id  # normalisation
        new_place = facade.create_place(place_data)

        return {
            "id": new_place.id,
            "title": new_place.title,
            "description": new_place.description,
            "price": new_place.price,
            "latitude": new_place.latitude,
            "longitude": new_place.longitude,
            "owner_id": getattr(new_place.owner_id, 'id', new_place.owner_id),
            "amenities": getattr(new_place, 'amenities', [])
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
                'owner_id': getattr(place.owner_id, 'id', place.owner_id),
                'amenities': getattr(place, 'amenities', [])
            })
        return result, 200

@api.route('/<string:place_id>')
@api.param('place_id', 'The Place identifier')
class PlaceDetail(Resource):
    @api.response(200, 'Place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Retrieve a place by its ID"""
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404

        return {
            "id": place.id,
            "title": place.title,
            "description": place.description,
            "price": place.price,
            "latitude": place.latitude,
            "longitude": place.longitude,
            "owner_id": getattr(place.owner_id, 'id', place.owner_id),
            "amenities": getattr(place, 'amenities', [])
        }, 200
