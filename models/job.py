from models import db
from datetime import datetime

class OffreEmploi(db.Model):
    __tablename__ = 'offres_emploi'
    
    id              = db.Column(db.Integer, primary_key=True)
    recruteur_id    = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    titre           = db.Column(db.String(200), nullable=False)
    entreprise      = db.Column(db.String(200))
    description     = db.Column(db.Text, nullable=False)
    type_contrat    = db.Column(db.String(50))  # CDI | CDD | Stage | Freelance
    secteur         = db.Column(db.String(100))
    ville           = db.Column(db.String(100), default='Niamey')
    salaire_min     = db.Column(db.Float)
    salaire_max     = db.Column(db.Float)
    experience      = db.Column(db.String(100))
    formation       = db.Column(db.String(200))
    competences     = db.Column(db.Text)
    date_limite     = db.Column(db.DateTime)
    telephone       = db.Column(db.String(20))
    email_contact   = db.Column(db.String(150))
    est_actif       = db.Column(db.Boolean, default=True)
    nb_vues         = db.Column(db.Integer, default=0)
    date_creation   = db.Column(db.DateTime, default=datetime.utcnow)