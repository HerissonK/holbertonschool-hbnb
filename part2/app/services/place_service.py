"""
Service : PlaceService
Gère la logique métier liée aux places (hébergements)
"""
from app.models.place import Place


class PlaceService:
    @staticmethod
    def create_place(data):
        """
        Crée un nouvel objet Place à partir des données reçues.
        """
        place = Place(
            title=data.get("title"),
            description=data.get("description", ""),
            price=data.get("price"),
            latitude=data.get("latitude"),
            longitude=data.get("longitude"),
            owner=data.get("owner_id"),
            amenities=data.get("amenities", [])
        )
        return place
