from app import create_app, db
from app.models.user import User
from app.models.amenity import Amenity

# Initialisation de l'app Flask et du contexte
app = create_app()

with app.app_context():
    print("🔄 Initialisation du contexte Flask...")

    # ===== 1️⃣ SUPPRESSION DE L'ANCIEN ADMIN =====
    old_admin = User.query.filter_by(email="admin@hbnb.com").first()
    if old_admin:
        db.session.delete(old_admin)
        db.session.commit()
        print("🗑️ Ancien admin supprimé.")
    else:
        print("✅ Aucun ancien admin trouvé.")

    # ===== 2️⃣ CRÉATION DU NOUVEL ADMIN =====
    admin = User(
        email="admin@hbnb.com",
        first_name="Super",
        last_name="Admin",
        is_admin=True
    )
    admin.password = "admin123"  # Setter qui hash le mot de passe
    db.session.add(admin)
    db.session.commit()

    print(f"✅ Nouvel admin créé : {admin.email} (id={admin.id})")

    # ===== 3️⃣ AJOUT DE 3 AMENITIES =====
    amenities = [
        Amenity(name="Wi-Fi"),
        Amenity(name="Piscine"),
        Amenity(name="Parking gratuit")
    ]

    for amenity in amenities:
        # éviter les doublons
        existing = Amenity.query.filter_by(name=amenity.name).first()
        if not existing:
            db.session.add(amenity)
            print(f"➕ Ajout de l'amenity : {amenity.name}")
        else:
            print(f"⚠️ Amenity '{amenity.name}' existe déjà, ignorée.")

    db.session.commit()
    print("✅ 3 amenities ajoutées avec succès.")

    # ===== 4️⃣ VÉRIFICATION =====
    print("\n=== Vérification ===")
    print("Admin présent ?", User.query.filter_by(is_admin=True).count() > 0)
    print("Total amenities :", Amenity.query.count())
    print("====================\n")

print("🌟 Script terminé avec succès.")
