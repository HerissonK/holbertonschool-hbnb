HBnB — Web Application

Cette application est une version simplifiée d’HBnB, permettant :

la gestion des utilisateurs (login)

l’affichage des logements

la consultation d’un logement

l’ajout de reviews (avis)

un filtrage par prix

une interface entièrement en HTML/CSS/JS vanilla

une API backend en Flask

🚀 Installation & Lancement
1. Installer les dépendances

Avant tout, assurez-vous d’avoir un environnement Python fonctionnel, ainsi que Flask, SQLAlchemy, etc.

pip install -r requirements.txt

2. Préparer la base de données

La première étape est de générer les tables ainsi que les données de base :

Étape 1 → Créer la base et les tables
python3 script.py

Étape 2 → Ajouter les lieux (places) dans la base
python3 add_places.py

Étape 3 → Lancer le serveur Flask
python3 run.py


Le serveur démarre sur :

http://127.0.0.1:5000


L’interface HTML doit être ouverte via un serveur local ou un simple navigateur.

🧪 Testing — Cas de test recommandés

Ci-dessous, tous les tests à effectuer pour valider la fonctionnalité complète de l’application.

🔐 1. Testing Login
🎯 Objectifs :

Vérifier que le système d’authentification fonctionne avec et sans erreurs.

✔ Cas de tests :
1.1 — Connexion avec identifiants valides

Aller sur login.html

Entrer un email et mot de passe valides

Vérifier :

que la requête renvoie un statut 200

que le JWT est bien stocké dans document.cookie

que l’utilisateur est redirigé vers index.html

1.2 — Connexion avec identifiants invalides

Entrer un mauvais mot de passe

Vérifier :

affichage du message d’erreur

absence du cookie token

🏠 2. Testing Index Page (index.html)
🎯 Objectifs :

Valider l’affichage de la liste des logements + le filtre + l’état de connexion.

✔ Cas de tests :
2.1 — Affichage des places

Se connecter depuis login.html

Arriver sur index.html

Vérifier :

que la liste des places se charge bien depuis /api/v1/places

2.2 — Filtre client-side sur le prix

Modifier le filtre “Max Price”

Vérifier :

que la liste se réduit automatiquement

qu’un message s’affiche si aucun résultat n’est trouvé

2.3 — Vérifier l’état de connexion dans le header

Connecté → le bouton Logout apparaît, le lien Login disparaît

Non connecté → seul le lien Login apparaît

🏡 3. Testing Place Detail Page (place.html)
🎯 Objectifs :

S’assurer que les détails du logement + les reviews s’affichent correctement.

✔ Cas de tests :
3.1 — Navigation vers un logement

Cliquer sur un logement depuis index

Vérifier que :

les infos (titre, description, prix, host, etc.) s’affichent

les reviews apparaissent correctement

3.2 — Formulaire d’ajout de review visible uniquement si authentifié

Si connecté : le formulaire “Add Review” apparaît

Si non connecté : il n’apparaît pas

⭐ 4. Testing Add Review
🎯 Objectifs :

Valider que seul un utilisateur connecté peut créer une review.

✔ Cas de tests :
4.1 — Ajouter un avis (utilisateur connecté)

Se connecter

Aller sur une page place

Remplir et envoyer le formulaire

Vérifier :

la review apparaît dans la liste immédiatement

le serveur renvoie un statut 201

le formulaire se vide automatiquement

4.2 — Tenter d’ajouter un avis (non connecté)

Se déconnecter

Aller sur place.html?id=xxx

Vérifier :

que le formulaire n’apparaît pas

ou que l’utilisateur est redirigé vers index.html

4.3 — Messages d’erreur

Entrer une note < 1 ou > 5

Vérifier le message d’erreur côté client

Tenter de reviewer le même logement 2 fois
→ Vérifier la réponse 409 et le message correspondant

🎉 Conclusion

Une fois tous les tests validés, votre projet HBnB est pleinement fonctionnel.