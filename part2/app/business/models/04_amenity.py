from core_model import BaseModel


class Amenity(BaseModel):
    def __init__(self, place_id, name, description):
        super().__init__()
        #self.__place_id = str(uuid.uuid4())
        self.comment = comment
        self.place = place
        self.date_creation = date_creation
        self.user = user
