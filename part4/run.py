from app import create_app, db
from flask import Flask
from flask_cors import CORS

app = create_app()

# ✅ active CORS (autorisera ton front à faire des requêtes depuis un autre port)
CORS(app, resources={r"/*": {"origins": "*"}})

if __name__ == "__main__":
    with app.app_context():
        # db.create_all()  # COMMENTÉ - Les tables existent déjà via le script SQL
        pass
    app.run(debug=True)