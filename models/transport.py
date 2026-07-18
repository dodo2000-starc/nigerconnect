from models import db
from datetime import datetime

class Trajet(db.Model):
    __tablename__ = 'trajets'
    
    id              = db.Column(db.Integer, primary_key=True)
    compagnie       = db.Column(db.String(200), nullable=False)
    type_transport  = db.Column(db.String(50))  # bus | taxi | moto
    depart          = db.Column(db.String(100), nullable=False)
    destination     = db.Column(db.String(100), nullable=False)
    date_depart     = db.Column(db.DateTime, nullable=False)
    places_total    = db.Column(db.Integer)
    places_dispo    = db.Column(db.Integer)
    prix            = db.Column(db.Float, nullable=False)
    telephone       = db.Column(db.String(20))
    est_actif       = db.Column(db.Boolean, default=True)
    date_creation   = db.Column(db.DateTime, default=datetime.utcnow)

class Livraison(db.Model):
    __tablename__ = 'livraisons'
    
    id              = db.Column(db.Integer, primary_key=True)
    expediteur_id   = db.Column(db.Integer, db.ForeignKey('users.id'))
    description     = db.Column(db.String(300))
    adresse_depart  = db.Column(db.String(300))
    adresse_arrivee = db.Column(db.String(300))
    poids           = db.Column(db.Float)
    prix            = db.Column(db.Float)
    statut          = db.Column(db.String(50), default='en_attente')
    code_suivi      = db.Column(db.String(20), unique=True)
    date_creation   = db.Column(db.DateTime, default=datetime.utcnow)
    date_livraison  = db.Column(db.DateTime)