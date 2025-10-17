from .core_model import BaseModel
import uuid
from typing import Optional

class Amenity(BaseModel):
    def __init__(self, name):
        super().__init__()
        self.name = name

def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }

def create_amenity(self, amenity_data):
    return self.amenity_repo.create(amenity_data)

def get_amenity(self, amenity_id):
    return self.amenity_repo.get(amenity_id)

def get_all_amenities(self):
    return self.amenity_repo.get_all()

def update_amenity(self, amenity_id, amenity_data):
    return self.amenity_repo.update(amenity_id, amenity_data)

def delete_amenity(self, amenity_id):
    return self.amenity_repo.delete(amenity_id)