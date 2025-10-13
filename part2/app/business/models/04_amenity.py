from core_model import BaseModel
from datetime import datetime


class Amenity(BaseModel):
    def __init__(self, name, description):
        super().__init__()
        #self.__review_id = str(uuid.uuid4())
        self.name = name
        #self.description = description à voir suivant le rendu
        #self.created_at = datetime.now()
        #self.updated_at = datetime.now()
