from app import db, bcrypt
import uuid

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    first_name = db.Column(db.String(128), nullable=False)
    last_name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    _password = db.Column("password", db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)

    # Relation avec Place
    places = db.relationship('Place', backref='owner', lazy=True)

    reviews = db.relationship('Review', backref='author', lazy=True)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, plain_password):
        hashed = bcrypt.generate_password_hash(plain_password)
        self._password = hashed.decode('utf-8') if isinstance(hashed, bytes) else hashed

    def verify_password(self, password):
        return bcrypt.check_password_hash(self._password, password)
