from models import db, bcrypt
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id            = db.Column(db.Integer, primary_key=True)
    nom           = db.Column(db.String(100), nullable=False)
    prenom        = db.Column(db.String(100), nullable=False)
    telephone     = db.Column(db.String(20), unique=True, nullable=False)
    email         = db.Column(db.String(150), unique=True, nullable=True)
    password_hash = db.Column(db.String(256), nullable=False)
    type_compte   = db.Column(db.String(50), default='citoyen')
    ville         = db.Column(db.String(100), default='Niamey')
    quartier      = db.Column(db.String(100))
    photo         = db.Column(db.String(200))
    is_active     = db.Column(db.Boolean, default=True)
    is_verified   = db.Column(db.Boolean, default=False)
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    derniere_connexion = db.Column(db.DateTime)
    
    # Relations
    annonces      = db.relationship('Annonce', backref='vendeur', lazy=True)
    offres_emploi = db.relationship('OffreEmploi', backref='recruteur', lazy=True)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def nom_complet(self):
        return f"{self.prenom} {self.nom}"

    def __repr__(self):
        return f'<User {self.telephone}>'