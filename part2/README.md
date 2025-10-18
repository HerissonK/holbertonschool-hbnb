# 🌆 HBNB - Partie 2 : API REST & Architecture en Couches

Hello ! \
Bienvenue dans la **partie 2 de notre projet HBnB** (clone de AirBnB version Holberton). Ici nous sommes partie d'une **code base** et nous avons du **implémenter différents endpoints**, gérer les **bons retours http** et surtout **assurer une bonne communication** entre **chaque couche** (Presentation, Business Logic et Persistance)


Cette partie du projetnous fait passer du modèle objet à la création d’une **API RESTful complète avec Flask**.
On met en place une **architecture en couches propre**, où chaque bloc a son rôle bien défini.

## ⚙️ Architecture en Couches


### **Principe des dépendances:**
```
┌─────────────────────────────────────┐
│   API (Présentation)                │  ← Couche 4
│   - Endpoints REST                  │
│   - Validation des entrées          │
└──────────────┬──────────────────────┘
               │ dépend de ↓
┌──────────────▼──────────────────────┐
│   Services (Business Logic)         │  ← Couche 3
│   - Logique métier                  │
│   - Orchestration                   │
└──────────────┬──────────────────────┘
               │ dépend de ↓
┌──────────────▼──────────────────────┐
│   Persistence (Storage Layer)       │  ← Couche 2
│   - Accès aux données               │
│   - CRUD operations                 │
└──────────────┬──────────────────────┘
               │ dépend de ↓
┌──────────────▼──────────────────────┐
│   Models (Entities)                 │  ← Couche 1
│   - Entités du domaine (ex: USER)   │
│   - Pas de dépendances externes     │
└─────────────────────────────────────┘
```

### 🗒️ *Point clé :*

* Une couche ne doit jamais importer une couche située au-dessus d’elle.
* Les imports suivent toujours le sens des flèches dans le schéma.

    *Exemple :*

    **api.v1.views.user** importe **models.user** \
    **models.user** importe **BaseModel** \
    **BaseModel** appelle **storage** pour la persistance \
    mais **storage** ne connaît jamais **Flask**


## 🌐 Endpoints disponibles
🧑‍💼 **USER**
```
Méthode |	Endpoint           	 | Description
GET	|    /api/v1/users	         | Liste tous les utilisateurs 
GET     |    /api/v1/users/<user_id>     | Récupère un utilisateur 
POST	|    /api/v1/users	         | Crée un nouvel utilisateur 
PUT	|    /api/v1/users/<user_id>	 | Met à jour un utilisateur 
DELETE	|    /api/v1/users/<user_id>	 | Supprime un utilisateur
```


🏡 **PLACE** 
```
Méthode |	Endpoint	        | Description
GET 	|   /api/v1/places	        | Liste des lieux 
GET	|   /api/v1/places/<place_id>	| Détail d’un lieu 
POST    |   /api/v1/places	        | Création d’un lieu 
PUT	|   /api/v1/places/<place_id>	| Mise à jour d’un lieu 
DELETE	|   /api/v1/places/<place_id>   | Suppression d’un lieu
```
💬 *Chaque Place est lié à un User (propriétaire) et à une City.*

⭐ **REVIEW**
```
Méthode   |	Endpoint                    | Description 
GET       |  /api/v1/reviews	            | Liste des avis 
POST	  |  /api/v1/reviews	            | Ajoute un avis 
DELETE	  |  /api/v1/reviews/<review_id>    | Supprime un avis
```

🧴 **AMENITY**
```
Méthode	  |        Endpoint                 | Description
GET	  | /api/v1/amenities	            | Liste des commodités
POST	  | /api/v1/amenities	            | Ajoute une commodité
PUT	  | /api/v1/amenities/<amenity_id>  | Met à jour une commodité
DELETE	  | /api/v1/amenities/<amenity_id>  | Supprime une commodité
```

## 🤓 Notes Techniques

 * Tous les retours sont au format JSON
 * Les erreurs (404, 400) sont gérées proprement
*  Blueprint utilisé pour séparer les routes par ressource



### Équipe 🤜🏼🤛🏼: 
Kevin et Arsinoé 
