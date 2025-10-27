# 🌆 HBnB, Auth & DB - Part 3

***L’objectif** de cette partie était de compléter notre application HBnB en intégrant :*

* Une **base de données relationnelle** pour **stocker les données** des utilisateurs, logements et réservations.
* La **mise en place d’endpoints sécurisés avec authentification** (login) et **protection des routes**.

*Cette étape nous a permis de **passer d’une version locale simple** vers une **architecture plus scalable et sécurisée***.

## 💻 Concepts clés vus et implémentés
🟣 **1. Gestion de la base de données** \
    - Utilisation de **MySQL pour stocker les données** de manière **relationnelle**. \
    - Utilisation de **SQLAlchemy ORM** pour **interagir avec la DB **et **gérer les relations** (*OneToMany, ManyToMany*).

*Exemple de relation :*
```
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(128), nullable=False, unique=True)
    places = relationship('Place', backref='owner', cascade='all, delete')
```

🟣 **2. Authentification et sécurité** \
    - **Implémentation d’un système de login avec JWT** (JSON Web Tokens).
    - **Protection des endpoints sensibles** grâce à un middleware qui vérifie le token.
    - **Stockage sécurisé** des mots de passe avec **hashing** (bcrypt).

*Flow principal :*
```
1. L’utilisateur envoie email + mot de passe à /login.
2. Si valide, un JWT est généré et renvoyé.
3. Chaque requête sur un endpoint protégé doit inclure le token dans les headers.
```
🟣 **3. Structure du projet**
```
HBnB/ 
│ 
├── app/ 
│   ├── models/ 
│   ├── API/v2 
│   ├── auth.py 
│   ├── db.py 
│   └── __init__.py 
│ 
├── tests/ 
│   └── TestAmenityEndpoints.py 
|   ├── TestPlaceEndpoints.py 
|   ├── TestReviewEndpoints.py 
|   ├── TestUserEndpoints.py 
│ 
├── requirements.txt 
├── config.py 
└── run.py 
```

* **models/ →** *définition des tables et relations SQLAlchemy*
* **routes/ →** *endpoints RESTful*
* **auth.py →** *gestion JWT et protection des routes*
* **db.py →** *configuration et initialisation de la DB*

## 🤜🏼🤛🏼 Conclusion

Merci d'être passer sur notre projet ! \
Si vous avez des idées d'amélioration ou bien des conseils à transmettre, nous serons ravie d'en échanger

**Kevin et Arsinoé**