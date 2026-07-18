from models import db
from datetime import datetime

class EtablissementSante(db.Model):
    __tablename__ = 'etablissements_sante'
    
    id            = db.Column(db.Integer, primary_key=True)
    nom           = db.Column(db.String(200), nullable=False)
    type_etab     = db.Column(db.String(100))  # hôpital | clinique | pharmacie | cabinet
    adresse       = db.Column(db.String(300))
    ville         = db.Column(db.String(100), default='Niamey')
    quartier      = db.Column(db.String(100))
    telephone     = db.Column(db.String(20))
    horaires      = db.Column(db.String(300))
    urgences      = db.Column(db.Boolean, default=False)
    latitude      = db.Column(db.Float)
    longitude     = db.Column(db.Float)
    est_actif     = db.Column(db.Boolean, default=True)
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    
    rendez_vous = db.relationship('RendezVousSante', backref='etablissement', lazy=True)

class RendezVousSante(db.Model):
    __tablename__ = 'rendez_vous_sante'
    
    id             = db.Column(db.Integer, primary_key=True)
    user_id        = db.Column(db.Integer, db.ForeignKey('users.id'))
    etablissement_id = db.Column(db.Integer, db.ForeignKey('etablissements_sante.id'))
    motif          = db.Column(db.String(300))
    date_rdv       = db.Column(db.DateTime, nullable=False)
    statut         = db.Column(db.String(50), default='en_attente')
    notes          = db.Column(db.Text)
    date_creation  = db.Column(db.DateTime, default=datetime.utcnow)