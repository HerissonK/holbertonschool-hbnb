"""
Service : ReviewService
Gère la logique métier liée aux avis (reviews)
"""
from app.models.review import Review


class ReviewService:
    @staticmethod
    def create_review(data):
        review = Review(
            user_id=data.get("user_id"),
            place_id=data.get("place_id"),
            text=data.get("text", "")
        )
        return review
