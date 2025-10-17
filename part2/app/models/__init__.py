"""
Couche Modèle - Entités du domaine
Pas de dépendances vers les autres couches
"""
from .core_model import BaseModel
from .place import Place
from .user import User
from .review import Review

__all__ = ['BaseModel', 'Place', 'User', 'Review']