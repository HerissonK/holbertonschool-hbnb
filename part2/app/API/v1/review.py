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
        new_review = facade.create_review(reviews_data)
        return {
            'text': new_review.text,
            'rating': new_reviews.rating,
            'user_id': new_reviews.user_id,
            'place_id': new_reviews.place_id
        }, 201

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        # Placeholder for logic to return a list of all reviews
        list_reviews = facade.get_all_reviews(reviews_data)
        if not list_reviews:
            {'error': 'Reviews not found!'}, 404

        return [
            {
                'text': new_review.text,
                'rating': new_reviews.rating,
                'user_id': new_reviews.user_id,
                'place_id': new_reviews.place_id
            }
            for r in list_reviews,
        ], 200


@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        # Placeholder for the logic to retrieve a review by ID
        reviews_by_id = facade.get_review(reviews_id)
        if not reviews_by_id:
            return {'error': "Review not found ¯\_(ツ)_/¯"}, 404

        return {
                'text': new_review.text,
                'rating': new_reviews.rating,
                'user_id': new_reviews.user_id,
                'place_id': new_reviews.place_id
        }, 200

    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update a review's information"""
        # Placeholder for the logic to update a review by ID
        data_review = api.payload
        updated = facade.update_review(data_review)
        if not updated_reviews:
            return {"error": "Review not found"}, 404

        update_review = facade.get_review(reviews_id)
        
        return {
                'text': updated_reviews.text,
                'rating': updated_review.rating,
                'user_id': updated_review.user_id,
                'place_id': updated_review.place_id
        }, 200

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review"""
        # Placeholder for the logic to delete a review
        pass

@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        # Placeholder for logic to return a list of reviews for a place
        pass