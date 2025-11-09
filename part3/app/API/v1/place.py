from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade
from app import db

api = Namespace('places', description='Place operations')

# Models pour Swagger
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(description='ID of the owner'),
    'amenities': fields.List(fields.String, required=True, description="List of amenities ID's")
})

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model)
    @jwt_required()
    def post(self):
        """Create a new place"""
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get("is_admin", False)
        place_data = api.payload

        # Vérifications des champs requis
        required_fields = ["title", "price", "latitude", "longitude"]
        for field in required_fields:
            if field not in place_data or place_data[field] in [None, ""]:
                return {"error": f"{field} is required"}, 400

        if place_data["price"] < 0:
            return {"error": "Price cannot be negative"}, 400

        owner_id = place_data.get("owner_id") or current_user_id
        owner = facade.get_user(owner_id)
        if not owner:
            return {"error": "Owner ID does not exist"}, 400

        # Vérification des amenities
        amenities_ids = place_data.get("amenities", [])
        amenities_objs = []
        for amenity_id in amenities_ids:
            amenity = facade.get_amenity(amenity_id)
            if not amenity:
                return {"error": f"Amenity with ID {amenity_id} does not exist"}, 400
            amenities_objs.append(amenity)

        place_data["owner_id"] = owner_id
        new_place = facade.create_place(place_data)

        # Associer les amenities
        new_place.amenities.extend(amenities_objs)
        db.session.commit()

        return {
            "id": new_place.id,
            "title": new_place.title,
            "description": new_place.description,
            "price": new_place.price,
            "latitude": new_place.latitude,
            "longitude": new_place.longitude,
            "owner_id": new_place.owner_id,
            "amenities": [{"id": a.id, "name": a.name} for a in new_place.amenities]
        }, 201

    def get(self):
        """Get all places"""
        places = facade.get_all_places()
        result = []
        for place in places:
            result.append({
                "id": place.id,
                "title": place.title,
                "description": place.description,
                "price": place.price,
                "latitude": place.latitude,
                "longitude": place.longitude,
                "owner_id": place.owner_id,
                "amenities": [{"id": a.id, "name": a.name} for a in getattr(place, 'amenities', [])]
            })
        return result, 200


@api.route('/<string:place_id>')
@api.param('place_id', 'The Place identifier')
class PlaceDetail(Resource):
    @api.response(200, 'Place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
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
            "owner_id": place.owner_id,
            "amenities": [{"id": a.id, "name": a.name} for a in getattr(place, 'amenities', [])]
        }, 200

    @api.expect(place_model)
    @jwt_required()
    def put(self, place_id):
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get("is_admin", False)

        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404

        # Vérifie que le user est admin ou propriétaire
        if not is_admin and place.owner_id != current_user_id:
            return {"error": "Unauthorized action"}, 403

        place_data = api.payload or {}
        allowed_fields = ["title", "description", "price", "latitude", "longitude", "owner_id", "amenities"]
        update_data = {k: v for k, v in place_data.items() if k in allowed_fields}

        # Validation simple
        if "price" in update_data and update_data["price"] < 0:
            return {"error": "Price cannot be negative"}, 400

        for coord in ["latitude", "longitude"]:
            if coord in update_data and not (-180 <= update_data[coord] <= 180 if coord == "longitude" else -90 <= update_data[coord] <= 90):
                return {"error": f"{coord} out of range"}, 400

        # Gestion des amenities
        amenities_objs = []
        if "amenities" in update_data:
            for amenity_id in update_data["amenities"]:
                amenity = facade.get_amenity(amenity_id)
                if not amenity:
                    return {"error": f"Amenity with ID {amenity_id} does not exist"}, 400
                amenities_objs.append(amenity)

        # Gestion propriétaire
        if "owner_id" in update_data:
            owner = facade.get_user(update_data["owner_id"])
            if not owner:
                return {"error": "Owner ID does not exist"}, 400
            place.owner_id = update_data["owner_id"]

        # Mise à jour des autres champs
        for key in ["title", "description", "price", "latitude", "longitude"]:
            if key in update_data:
                setattr(place, key, update_data[key])

        # Mettre à jour amenities
        if amenities_objs:
            place.amenities.clear()
            place.amenities.extend(amenities_objs)

        db.session.commit()

        return {
            "id": place.id,
            "title": place.title,
            "description": place.description,
            "price": place.price,
            "latitude": place.latitude,
            "longitude": place.longitude,
            "owner_id": place.owner_id,
            "amenities": [{"id": a.id, "name": a.name} for a in place.amenities]
        }, 200
