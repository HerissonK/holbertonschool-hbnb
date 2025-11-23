from app import create_app, db
from app.models.user import User
from app.models.place import Place
from app.models.amenity import Amenity
import uuid

app = create_app()

with app.app_context():

    print("🔄 Initialisation du contexte Flask...")

    db.create_all()
    print("📦 Tables vérifiées.")

    # === 1️⃣ CRÉATION UTILISATEUR ===
    email = "user@example.com"
    user = User.query.filter_by(email=email).first()

    if not user:
        user = User(
            id=str(uuid.uuid4()),
            email=email,
            first_name="John",
            last_name="Doe",
            is_admin=False
        )
        user.password = "user123"
        db.session.add(user)
        db.session.commit()
        print(f"👤 Utilisateur créé : {email}")
    else:
        print(f"⚠️ Utilisateur {email} déjà existant.")

    # === 2️⃣ RÉCUPÉRATION AMENITIES ===
    amenities = Amenity.query.all()

    if not amenities:
        print("❌ Aucune amenity trouvée ! Exécute d’abord le script précédent.")
        exit()

    print(f"🔧 {len(amenities)} amenities disponibles.")

    # === 3️⃣ DONNÉES DES PLACES ===
    places_data = [
        {
            "title": "Cozy Apartment",
            "description": "A warm and comfortable apartment downtown.",
            "price": 80.0,
            "latitude": 48.8566,
            "longitude": 2.3522
        },
        {
            "title": "Luxury Villa",
            "description": "Spacious villa with private swimming pool.",
            "price": 240.0,
            "latitude": 43.2965,
            "longitude": 5.3698
        },
        {
            "title": "Forest Cabin",
            "description": "Rustic cabin perfect for nature lovers.",
            "price": 60.0,
            "latitude": 45.7640,
            "longitude": 4.8357
        },
        {
            "title": "Modern Studio",
            "description": "Small modern studio with a great view.",
            "price": 55.0,
            "latitude": 44.8378,
            "longitude": -0.5792
        }
    ]

    # === 4️⃣ CRÉATION DES PLACES ===
    for i, data in enumerate(places_data):
        place = Place(
            id=str(uuid.uuid4()),
            title=data["title"],
            description=data["description"],
            price=data["price"],
            latitude=data["latitude"],
            longitude=data["longitude"],
            owner_id=user.id
        )


        # Associer une amenity par place
        amenity = amenities[i % len(amenities)]
        place.amenities.append(amenity)

        db.session.add(place)

        print(f"🏠 Place créée : {place.title} (amenity: {amenity.name})")

    db.session.commit()
    print("✅ Toutes les places ont été ajoutées.")

    print("\n=== Vérification ===")
    print("Utilisateurs :", User.query.count())
    print("Places :", Place.query.count())
    print("Amenities :", Amenity.query.count())
    print("====================\n")

print("🌟 Script terminé avec succès.")
