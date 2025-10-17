from .core_model import BaseModel
from datetime import datetime
import uuid

from app.models.core_model import BaseModel

class User(BaseModel):
    def __init__(self, first_name, last_name, email, id=None):
        super().__init__()
        self.id = id or str(uuid.uuid4())
        self.first_name = first_name
        self.last_name = last_name
        self.email = email


    def update(self, data):
        for key, value in data.items():
            if key != "id":
                setattr(self, key, value)