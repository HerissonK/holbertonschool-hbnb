from app import db, bcrypt
import uuid

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    first_name = db.Column(db.String(128), nullable=False)
    last_name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    _password = db.Column(db.String(128), name='password', nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)

    # One to Many relationship
    places = db.relationship('Place', backref='owner', lazy=True)
    reviews = db.relationship('Review', backref='author', lazy=True)

    def update(self, data):
        for key, value in data.items():
            if key != "id":
                setattr(self, key, value)

    @property
    def password(self):
        """Empêche la lecture du mot de passe"""
        return self._password

    @password.setter
    def password(self, plain_password):
        """Hash automatiquement le mot de passe quand on le définit"""
        hashed = bcrypt.generate_password_hash(plain_password)
        # Compatible toutes versions de flask-bcrypt
        self._password = hashed.decode('utf-8') if isinstance(hashed, bytes) else hashed

    def verify_password(self, password):
        """Vérifie si le mot de passe correspond au hash"""
        return bcrypt.check_password_hash(self._password, password)