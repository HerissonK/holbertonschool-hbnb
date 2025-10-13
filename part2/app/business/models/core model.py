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
    def create(self, data):
        """Create a futur object"""
        self.created_at = datatime.now()
        self.save()

    def update(self, data):
        """Update the attributes of the object based on the provided dictionary"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()  # Update the updated_at timestamp

    # GET
    def get_object(self, data):
        """Get an object"""
        self.create(data)

    # DEL
    def delete_object(self, data):
        """Delete the object"""
        del self.get_object(data)
