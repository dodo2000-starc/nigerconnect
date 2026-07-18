from models import db
from datetime import datetime

class Prestataire(db.Model):
    __tablename__ = 'prestataires'
    
    id               = db.Column(db.Integer, primary_key=True)
    user_id          = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    service_type     = db.Column(db.String(100), nullable=False)
    specialites      = db.Column(db.String(300))
    description      = db.Column(db.Text)
    experience_years = db.Column(db.Integer, default=0)
    tarif_min        = db.Column(db.Float)
    tarif_max        = db.Column(db.Float)
    disponible       = db.Column(db.Boolean, default=True)
    ville            = db.Column(db.String(100), default='Niamey')
    quartier         = db.Column(db.String(100))
    telephone        = db.Column(db.String(20))
    note_moyenne     = db.Column(db.Float, default=0.0)
    nb_missions      = db.Column(db.Integer, default=0)
    est_verifie      = db.Column(db.Boolean, default=False)
    date_creation    = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relations
    user     = db.relationship('User', backref='prestataires_profils', lazy=True)
    demandes = db.relationship('DemandeService', backref='prestataire', lazy=True)


class DemandeService(db.Model):
    __tablename__ = 'demandes_service'
    
    id             = db.Column(db.Integer, primary_key=True)
    client_id      = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    prestataire_id = db.Column(db.Integer, db.ForeignKey('prestataires.id'), nullable=False)
    description    = db.Column(db.Text, nullable=False)
    adresse        = db.Column(db.String(300))
    date_souhaitee = db.Column(db.DateTime)
    budget         = db.Column(db.Float)
    statut         = db.Column(db.String(50), default='en_attente')
    date_creation  = db.Column(db.DateTime, default=datetime.utcnow)
    date_resolution = db.Column(db.DateTime)
    note_client    = db.Column(db.Integer)
    commentaire_client = db.Column(db.Text)
    
    # Relation
    client = db.relationship('User', foreign_keys=[client_id], backref='demandes_faites', lazy=True)