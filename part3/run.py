from app import create_app, db

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Crée les tables s'il n'y en a pas
    app.run(debug=True)
