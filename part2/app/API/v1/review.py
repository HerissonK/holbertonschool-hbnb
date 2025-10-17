from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('reviews', description='Review operations')

# Modèle Swagger / validation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new review"""
        review_data = api.payload

        # Champs obligatoires
        required_fields = ['user_id', 'place_id', 'text', 'rating']
        for field in required_fields:
            if field not in review_data or review_data[field] in ("", None):
                return {"error": f"{field.replace('_', ' ').capitalize()} is required"}, 400

        # Vérification rating
        rating = review_data.get('rating')
        if not isinstance(rating, int) or not (1 <= rating <= 5):
            return {"error": "Rating must be an integer between 1 and 5"}, 400

        new_review = facade.create_review(review_data)
        return new_review.to_dict(), 201

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        list_reviews = facade.get_all_reviews()
        if not list_reviews:
            return {'error': 'Reviews not found!'}, 404

        return [review.to_dict() for review in list_reviews], 200

@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        review = facade.get_review(review_id)
        if not review:
            return {'error': "Review not found"}, 404
        return review.to_dict(), 200

    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        data_review = api.payload
        updated_review = facade.update_review(review_id, data_review)
        if not updated_review:
            return {"error": "Review not found"}, 404
        return {"message": "Review updated successfully", "updated_at": updated_review.updated_at.isoformat()}, 200

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        deleted = facade.delete_review(review_id)
        if not deleted:
            return {"message": "Review not found"}, 404
        return {"message": "Review deleted successfully"}, 200
