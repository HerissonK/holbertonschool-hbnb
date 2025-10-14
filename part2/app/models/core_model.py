import uuid
from datetime import datetime


data = {}


class BaseModel:
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    # PATCH
    def save(self):
        """Update the updated_at timestamp whenever the object is modified"""
        self.updated_at = datetime.now()

    # POST 
    @classmethod
    def create(cls, **kwargs):
        """Crée et retourne une nouvelle instance"""
        instance = cls(**kwargs)
        return instance

    def update(self, **kwargs):
        """Met à jour les attributs de l'objet"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()

    # GET
    @classmethod
    def get_object(cls, object_id):
        """Récupère un objet depuis le stockage"""
        return data.get(object_id)

    # DEL
    @classmethod
    def delete(cls, object_id):
        """Supprime un objet du stockage"""
        if object_id in data:
            del data[object_id]

