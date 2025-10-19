from flask_restx import Namespace, Resource, fields
from app.services.facade import facade

api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new amenity"""  

        amenity_data = api.payload
        required_fields = ["name"]

        for field in required_fields:
            value = amenity_data.get(field, "").strip()
            if not value:
                return {"error": f"{field.replace('_', ' ').capitalize()} is required"}, 400

        new_amenity = facade.create_amenity(amenity_data)
        return {"id": new_amenity.id, "name": new_amenity.name, "created_at": new_amenity.created_at.isoformat()}, 201

@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        return {'id': amenity.id, 'name': amenity.name}, 200

    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """Update an amenity's information"""
        amenity_data = api.payload
        updated = facade.update_amenity(amenity_id, amenity_data)
        if not updated:
            return {'error': 'Amenity not found'}, 404

    # Verification du remplissage de la totalite des champs
        required_fields = ['id', 'name']
        for field in required_fields:
            if field not in amenity_review or amenity_review[field] in ("", None):
                return {"error": f"{field.replace('_', ' ').capitalize()} is required"}, 400

        amenity = facade.get_amenity(amenity_id)

        return {'id': amenity.id, 'name': amenity.name, 'updated_at': amenity.updated_at.isoformat()}, 200
