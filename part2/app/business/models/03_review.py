from core_model import BaseModel


class Amenity(BaseModel):
    def __init__(self, name, description):
        super().__init__()
        #self.__review_id = str(uuid.uuid4())
        self.name = name
        self.description = description