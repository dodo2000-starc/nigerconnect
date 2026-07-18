from models import db
from datetime import datetime

class EntrepriseAnnuaire(db.Model):
    __tablename__ = 'entreprises_annuaire'
    
    id            = db.Column(db.Integer, primary_key=True)
    user_id       = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    nom           = db.Column(db.String(200), nullable=False)
    categorie     = db.Column(db.String(100), nullable=False)
    # Pharmacie | Hôtel | Restaurant | École | Garage | Service public | Boutique | Autre
    description   = db.Column(db.Text)
    telephone     = db.Column(db.String(20))
    telephone2    = db.Column(db.String(20))
    email         = db.Column(db.String(150))
    site_web      = db.Column(db.String(200))
    adresse       = db.Column(db.String(300))
    ville         = db.Column(db.String(100), default='Niamey')
    quartier      = db.Column(db.String(100))
    latitude      = db.Column(db.Float)
    longitude     = db.Column(db.Float)
    horaires      = db.Column(db.String(300))
    logo          = db.Column(db.String(200))
    est_verifie   = db.Column(db.Boolean, default=False)
    est_premium   = db.Column(db.Boolean, default=False)
    nb_vues       = db.Column(db.Integer, default=0)
    note_moyenne  = db.Column(db.Float, default=0.0)
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    
    avis = db.relationship('AvisAnnuaire', backref='entreprise', lazy=True)

class AvisAnnuaire(db.Model):
    __tablename__ = 'avis_annuaire'
    
    id            = db.Column(db.Integer, primary_key=True)
    entreprise_id = db.Column(db.Integer, db.ForeignKey('entreprises_annuaire.id'))
    user_id       = db.Column(db.Integer, db.ForeignKey('users.id'))
    note          = db.Column(db.Integer)  # 1 à 5
    commentaire   = db.Column(db.Text)
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)