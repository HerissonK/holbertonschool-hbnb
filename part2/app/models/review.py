from .core_model import BaseModel
from datetime import datetime


class Review(BaseModel):
    def __init__(self, text, place, rating, user):
        super().__init__()
        # self.__place_id = str(uuid.uuid4())
        self.text = text
        self.place = place
        self.rating = rating
        #self.date_creation = date_creation BONUS revoir l'utilitée
        self.user = user
        #self.created_at = datetime.now()
        #self.updated_at = datetime.now()
