from app import db, bcrypt
import uuid

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    first_name = db.Column(db.String(128), nullable=False)
    last_name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)

    # One to Many relationship
    places = db.relationship('Place', backref='owner', lazy=True)
    reviews = db.relationship('Review', backref='author', lazy=True)
    def update(self, data):
        for key, value in data.items():
            if key != "id":
                setattr(self, key, value)
    
    @property
    def password_hash(self):
        raise AttributeError("Password is write-only")

    @password_hash.setter
    def password_hash(self, plain_password):
        """Hash automatiquement le mot de passe quand on le définit"""
        self.password = bcrypt.generate_password_hash(plain_password).decode("utf-8")

    def verify_password(self, password):
        """Vérifie si le mot de passe correspond au hash"""
        return bcrypt.check_password_hash(self.password, password)

    