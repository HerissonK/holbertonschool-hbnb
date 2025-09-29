# 🌆 HBnB – Clone d'Airbnb

Bienvenue dans le **projet HBnB**, \
une application inspirée d'Airbnb qui nous **accompagne tout au long de notre parcours d'apprentissage** en **développement web**. \
Ce projet est conçu pour **évoluer étape par étape** : \
de la simple **base de données** jusqu'à une **application web** complète avec **API**, **interface** et **intégration avancée**.

## 🌱 Objectifs du projet

### **L'objectif principal est de :**

Comprendre et appliquer une **architecture en couches** (présentation, logique métier, persistance). \
Construire progressivement un **clone simplifié d'Airbnb** (HBnB Evolution). \
Apprendre à **travailler en équipe**, avec des rôles définis et des livrables clairs. \
Mettre en pratique les principes de **POO**, la **documentation UML**, la **gestion de donnée**s, et la création d'**API RESTful**.


**Gestion des utilisateurs**
💻

    - Inscription, connexion et mise à jour de profil.
    - Différenciation entre utilisateurs classiques et administrateurs.

**Gestion des lieux** (places) 🗺️

    - Création, modification, suppression et affichage.
    - Informations clés : titre, description, prix, latitude, longitude.
    - Association avec un propriétaire (utilisateur).
    - Ajout de commodités (amenities).

**Gestion des avis** ⭐

    - Chaque utilisateur peut laisser un avis (rating + commentaire) sur un lieu.
    - Avis liés à la fois à un utilisateur et à un lieu.

**Gestion des commodités** 🛋️

    - Ajout, suppression et modification d'amenities.
    - Association avec les lieux.


## ⚙️ Architecture du projet

### **HBnB repose sur une architecture en trois couches :**

**Présentation :**

    - API et services accessibles aux utilisateurs.
    - Interface web à venir dans les étapes suivantes.

**Logique métier :**

    - Gestion des entités (User, Place, Review, Amenity).
    - Application des règles métier.

**Persistance :**

    - Stockage dans une base de données.
    - Gestion de la création, mise à jour et suppression des données.

💡 Les couches interagissent grâce au facade pattern, garantissant une séparation claire des responsabilités.


## 🌷 Évolution du projet

### HBnB est divisé en plusieurs parties :

    1. UML & Documentation technique

        - Diagrammes de packages, classes et séquence.
        - Base de réflexion sur l'architecture.

    2. Base de données & ORM

        - Mise en place du modèle de données.
        - Gestion de la persistance.

    3. API RESTful

        - Exposition des services pour manipuler les entités.
        - Tests manuels et automatiques.

    4. Interface Web

        - Développement du front-end.
        - Intégration avec l'API.

    5. Fonctionnalités avancées

        - Authentification sécurisée.
        - Filtres, recherche, amélioration des performances.


## 🔧 Outils et technologies

**Langage :** *Python (backend)* \
**UML :** *Mermaid.js* \
**Framework Web :** *Flask ou Django* \
**Base de données :** *MySQL / PostgreSQL* \
**Front-end :** *HTML, CSS, JavaScript* 

## 👥 Équipe

**Arsinoe Chobert**  \
**Kevin Herisson** 

**Notre état d'esprit :***

HBnB, ce n'est pas seulement un projet technique :
C'est l'occasion d'**apprendre à travailler en équipe**, à **structurer un projet logiciel** et à **monter en compétence** étape par étape.
