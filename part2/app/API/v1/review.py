# SAVING DE REVIEW API 

from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
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
        # Placeholder for the logic to register a new review
        review_data = api.payload
        new_review = facade.create_review(review_data)

        required_fields = ['user_id', 'place_id', 'rating']

        rating = review_data.get('rating')
        if rating in ("", None):
            return {"error": "Rating is required"}, 400

        if not isinstance(rating, int) or not (1 <= rating <= 5):
            return {"error": "Rating must be an integer between 1 and 5"}, 400

        for field in required_fields:
            if field not in review_data or review_data[field] in ("", None):
                return {"error": f"{field.replace('_', ' ').capitalize()} is required"}, 400
        
        return {
            'id': new_review.id,
            'text': new_review.text,
            'rating': new_review.rating,
            'user_id': new_review.user_id,
            'place_id': new_review.place_id,
            'create_at': new_review.created_at.isoformat()
        }, 201

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        # Placeholder for logic to return a list of all reviews
        list_reviews = facade.get_all_reviews()
        if not list_reviews:
            return {'error': 'Reviews not found!'}, 404

        return [
            {
                'text': review.text,
                'rating': review.rating,
            }
            for review in list_reviews
        ], 201


@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        # Placeholder for the logic to retrieve a review by ID
        review = facade.get_review(review_id)
        if not review:
            return {'error': "Review not found"}, 404

        return {
                'id': review.id,
                'text': review.text,
                'rating': review.rating,
                'user_id': review.user_id,
                'place_id': review.place_id
        }, 201

    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update a review's information"""
        # Placeholder for the logic to update a review by ID
        data_review = api.payload
        updated_review = facade.update_review(review_id, data_review)
        if not updated_review:
            return {"error": "Review not found"}, 404

        required_fields = ['user_id', 'place_id', 'text']
        for field in required_fields:
            if field not in data_review or data_review[field] in ("", None):
                return {"error": f"{field.replace('_', ' ').capitalize()} is required"}, 400

        text = data_review.get('text')
        if text in ("", None):
            return {"error": "Comment is required"}, 400

        if not isinstance(text, str):
            return {"error": "The comment should a text"}, 400

        return {
                "message": "Review updated successfully",
                "updated_at": review.updated_at.isoformat()
        }, 201

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def delete(self, review_id):
        """Delete a review"""
        # Placeholder for the logic to delete a review
        review = api.payload
        if not review:
            {"message": "Review not found"}

        review_to_delete = facade.delete_review(review_id)
        return {
            "message": "Review deleted successfully"
        }, 200


@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        # Placeholder for logic to return a list of reviews for a place
        reviews = facade.get_reviews_by_place(place_id)
        if not reviews:
            return {'message': 'No review found for this place'}, 200

        return [
            {
                'id': review.id,
                'text': review.text,
                'rating': review.rating,
            }
            for review in reviews
        ], 200
