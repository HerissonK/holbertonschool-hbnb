from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('places', description='Place operations')

# Models Swagger
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

place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(required=True, description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.String, description="List of amenities IDs")
})

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Create a new place"""
        place_data = api.payload
        required_fields = ["title", "description", "price", "latitude", "longitude", "owner_id"]

        # Vérifie les champs requis
        for field in required_fields:
            value = place_data.get(field)
            if value is None or (isinstance(value, str) and not value.strip()):
                return {"error": f"{field.replace('_', ' ').capitalize()} is required"}, 400

        # Vérifie types numériques
        for field in ["price", "latitude", "longitude"]:
            if not isinstance(place_data[field], (int, float)):
                return {"error": f"{field.replace('_', ' ').capitalize()} must be a number"}, 400

        # Prix positif
        if place_data["price"] < 0:
            return {"error": "Price cannot be negative"}, 400

        # Vérifie si le owner existe
        owner = facade.get_user(place_data["owner_id"])
        if not owner:
            return {"error": "Owner not found"}, 400

        # Crée la place
        new_place = facade.create_place(place_data)
        return new_place.to_dict(), 201

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """List all places"""
        places = facade.get_all_places()
        return [p.to_dict() for p in places], 200


@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404
        return place.to_dict(), 200

    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update a place"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        data = api.payload
        required_fields = ["title", "description", "price", "latitude", "longitude"]
        for field in required_fields:
            if field not in data or data[field] in ("", None):
                return {"error": f"{field.replace('_', ' ').capitalize()} is required"}, 400

        updated_place = facade.update_place(place_id, data)
        return updated_place.to_dict(), 200

    @api.response(200, 'Place deleted successfully')
    @api.response(404, 'Place not found')
    def delete(self, place_id):
        """Delete a place"""
        deleted = facade.delete_place(place_id)
        if not deleted:
            return {"error": "Place not found"}, 404
        return {"message": "Place deleted successfully"}, 200
