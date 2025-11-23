from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade

api = Namespace('reviews', description='Review operations')

# --- Model pour Swagger ---
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'place_id': fields.String(required=True, description='ID of the place')
})

# =============================
#       CREATE & LIST ALL
# =============================
@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        """Create a new review"""
        review_data = api.payload
        current_user_id = get_jwt_identity()

        # --- Validation des champs ---
        place_id = review_data.get("place_id")
        rating = review_data.get("rating")
        text = review_data.get("text", "")

        if not place_id:
            return {"error": "Place ID is required"}, 400
        if not isinstance(rating, int) or not (1 <= rating <= 5):
            return {"error": "Rating must be an integer between 1 and 5"}, 400

        # --- Vérifie que le lieu existe ---
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404

        # --- L'utilisateur ne peut pas noter son propre lieu ---
        if place.owner_id == current_user_id:
            return {"error": "You cannot review your own place"}, 403

        # --- Vérifie si l'utilisateur a déjà noté ---
        already_review = facade.get_review_by_user_and_place(current_user_id, place_id)
        if already_review:
            return {"error": "You have already reviewed this place"}, 409

        # --- Crée la review ---
        new_review = facade.create_review({
            "user_id": current_user_id,
            "place_id": place_id,
            "rating": rating,
            "text": text
        })

        user = facade.get_user(current_user_id)
        user_name = f"{user.first_name} {user.last_name}" if user else "Anonymous"

        return {
            'id': new_review.id,
            'text': new_review.text,
            'rating': new_review.rating,
            'user_id': new_review.user_id,
            'place_id': new_review.place_id,
            'user_name': user_name
        }, 201

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve all reviews"""
        reviews = facade.get_all_reviews()
        if not reviews:
            return {'message': 'No reviews found'}, 200

        results = []
        for review in reviews:
            user = facade.get_user(review.user_id)
            user_name = f"{user.first_name} {user.last_name}" if user else "Anonymous"
            results.append({
                'id': review.id,
                'text': review.text,
                'rating': review.rating,
                'place_id': review.place_id,
                'user_name': user_name
            })

        return results, 200


# =============================
#       GET / UPDATE / DELETE
# =============================
@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': "Review not found"}, 404

        user = facade.get_user(review.user_id)
        user_name = f"{user.first_name} {user.last_name}" if user else "Anonymous"

        return {
            'id': review.id,
            'text': review.text,
            'rating': review.rating,
            'user_id': review.user_id,
            'place_id': review.place_id,
            'user_name': user_name
        }, 200

    @api.expect(review_model)
    @jwt_required()
    def put(self, review_id):
        """Update a review"""
        current_user = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get("is_admin", False)
        review_data = api.payload

        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404

        if not is_admin and review.user_id != current_user:
            return {"error": "You can only modify your own reviews"}, 403

        text = review_data.get("text", "")
        rating = review_data.get("rating")

        if not text:
            return {"error": "Comment text is required"}, 400
        if not isinstance(rating, int) or not (1 <= rating <= 5):
            return {"error": "Rating must be an integer between 1 and 5"}, 400

        review.text = text
        review.rating = rating
        facade.review_repo.add(review)

        return {"message": "Review updated successfully"}, 200

    @jwt_required()
    def delete(self, review_id):
        """Delete a review"""
        current_user = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get("is_admin", False)

        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404

        if not is_admin and review.user_id != current_user:
            return {"error": "Unauthorized action"}, 403

        facade.delete_review(review_id)
        return {"message": "Review deleted successfully"}, 200


# =============================
#       GET BY PLACE
# =============================
@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        reviews = facade.get_reviews_by_place(place_id)
        if not reviews:
            return {'message': 'No review found for this place'}, 200

        results = []
        for review in reviews:
            user = facade.get_user(review.user_id)
            user_name = f"{user.first_name} {user.last_name}" if user else "Anonymous"
            results.append({
                'id': review.id,
                'text': review.text,
                'rating': review.rating,
                'user_id': review.user_id,
                'place_id': review.place_id,
                'user_name': user_name
            })

        return results, 200
