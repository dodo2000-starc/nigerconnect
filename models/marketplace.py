from models import db
from datetime import datetime

class Annonce(db.Model):
    __tablename__ = 'annonces'
    
    id            = db.Column(db.Integer, primary_key=True)
    user_id       = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    titre         = db.Column(db.String(200), nullable=False)
    description   = db.Column(db.Text, nullable=False)
    prix          = db.Column(db.Float, nullable=False)
    prix_negociable = db.Column(db.Boolean, default=False)
    categorie     = db.Column(db.String(100), nullable=False)
    # Immobilier | Véhicule | Agriculture | Électronique | Mobilier | Vêtements | Autre
    sous_categorie = db.Column(db.String(100))
    etat          = db.Column(db.String(50), default='Neuf')
    # Neuf | Bon état | Usage
    ville         = db.Column(db.String(100), default='Niamey')
    quartier      = db.Column(db.String(100))
    telephone     = db.Column(db.String(20))
    images        = db.Column(db.Text)  # JSON liste des images
    statut        = db.Column(db.String(50), default='active')
    # active | vendu | suspendu
    nb_vues       = db.Column(db.Integer, default=0)
    est_premium   = db.Column(db.Boolean, default=False)
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    date_expiration = db.Column(db.DateTime)