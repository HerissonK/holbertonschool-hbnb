from app import db, bcrypt
import uuid

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    first_name = db.Column(db.String(128), nullable=False)
    last_name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    _password = db.Column("password", db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def update(self, data):
        for key, value in data.items():
            if key != "id":
                setattr(self, key, value)
    
    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, plain_password):
        """Hash automatiquement le mot de passe quand on le définit"""
        self._password = bcrypt.generate_password_hash(plain_password).decode("utf-8")

    def verify_password(self, password):
        """Vérifie si le mot de passe correspond au hash."""
        return bcrypt.check_password_hash(self._password, password)
