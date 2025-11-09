# SAVING DE REVIEW API 

from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
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
    @jwt_required()
    def post(self):
        """Register a new review"""
        # Placeholder for the logic to register a new review
        review_data = api.payload
        current_user = get_jwt_identity()

        place_id = review_data.get("place_id")
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404

        required_fields = ['place_id', 'rating']
        for field in required_fields:
            if field not in review_data or review_data[field] in ("", None):
                return {"error": f"{field.replace('_', ' ').capitalize()} is required"}, 400

        rating = review_data.get('rating')
        if rating in ("", None):
            return {"error": "Rating is required"}, 400

        if not isinstance(rating, int) or not (1 <= rating <= 5):
            return {"error": "Rating must be an integer between 1 and 5"}, 400

        # Check if the user review it own place
        if place.user_id == current_user:
            return {"error": "You cannot review your own place"}, 403

        # Check if the user already rates this place
        already_review = facade.get_review_by_user_and_place(current_user, place.id)
        if already_review:
            return {"error": "You have already reviewed this place"}, 409
        
        new_review = facade.create_review({
            "user_id": current_user,
            "place_id": place.id,
            "rating": rating,
            "text": review_data.get("text", "")
        })

        return {
            'id': new_review.id,
            'text': new_review.text,
            'rating': new_review.rating,
            'user_id': new_review.user_id,
            'place_id': new_review.place_id
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
                'id': review.id,
                'text': review.text,
                'rating': review.rating,
                'place_id': review.place_id
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
    @jwt_required()
    def put(self, review_id):
        """Update a review's information"""
        current_user = get_jwt_identity()
        check_is_admin = get_jwt()
        is_admin = check_is_admin.get("is_admin", False)

        # ✅ On récupère d'abord le body
        review_data = api.payload

        # ✅ On récupère ensuite la review existante
        updated_review = facade.get_review(review_id)
        if not updated_review:
            return {"error": "Review not found"}, 404

        # ✅ Vérifie que l’utilisateur est bien le propriétaire ou admin
        if not is_admin and updated_review.user_id != current_user:
            return {"error": "You can only modify your reviews"}, 403

        # ✅ Validation des champs
        allowed_fields = ["text", "rating"]

        if "rating" in review_data:
            rating = review_data["rating"]
            if not isinstance(rating, int) or not (1 <= rating <= 5):
                return {"error": "Rating must be an integer between 1 and 5"}, 400

        text = review_data.get("text", "")
        if text in ("", None):
            return {"error": "Comment is required"}, 400
        if not isinstance(text, str):
            return {"error": "The comment should be a text"}, 400

        # ✅ Mise à jour des champs autorisés
        for field in allowed_fields:
            if field in review_data:
                setattr(updated_review, field, review_data[field])

        # ✅ Sauvegarde dans la base via le repo
        facade.review_repo.add(updated_review)

        return {
            "message": "Review updated successfully",
            "updated_at": updated_review.updated_at.isoformat()
        }, 200


    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def delete(self, review_id):
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get("is_admin", False)

        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404

        # Vérification des permissions
        if not is_admin and review.user_id != current_user_id:
            return {"error": "Unauthorized action"}, 403

        facade.delete_review(review_id)
        return {"message": "Review deleted successfully"}, 200



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
