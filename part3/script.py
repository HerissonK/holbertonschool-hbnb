from app import create_app, db
from app.models.user import User
from app.models.amenity import Amenity
import uuid

# Initialisation de l'app Flask et du contexte
app = create_app()

with app.app_context():
    print("🔄 Initialisation du contexte Flask...")

    # === Création des tables si elles n'existent pas ===
    db.create_all()
    print("📦 Tables créées (si manquantes).")

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
    admin.password = "admin123"  # setter qui hash le mot de passe
    db.session.add(admin)
    db.session.commit()
    print(f"✅ Nouvel admin créé : {admin.email} (id={admin.id})")

    # ===== 3️⃣ AJOUT DE 3 AMENITIES AVEC ID =====
    amenities_data = [
        {"id": str(uuid.uuid4()), "name": "Wi-Fi"},
        {"id": str(uuid.uuid4()), "name": "Piscine"},
        {"id": str(uuid.uuid4()), "name": "Parking gratuit"},
    ]

    for data in amenities_data:
        existing = Amenity.query.filter_by(name=data["name"]).first()
        if not existing:
            amenity = Amenity(id=data["id"], name=data["name"])
            db.session.add(amenity)
            print(f"➕ Ajout de l'amenity : {data['name']} (id={data['id']})")
        else:
            print(f"⚠️ Amenity '{data['name']}' existe déjà, ignorée.")

    db.session.commit()
    print("✅ 3 amenities ajoutées avec succès.")

    # ===== 4️⃣ VÉRIFICATION =====
    print("\n=== Vérification ===")
    print("Admin présent ?", User.query.filter_by(is_admin=True).count() > 0)
    print("Total amenities :", Amenity.query.count())
    print("====================\n")

print("🌟 Script terminé avec succès.")
