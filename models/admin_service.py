from models import db
from datetime import datetime

class DemarcheAdmin(db.Model):
    __tablename__ = 'demarches_admin'
    
    id            = db.Column(db.Integer, primary_key=True)
    titre         = db.Column(db.String(200), nullable=False)
    description   = db.Column(db.Text, nullable=False)
    ministere     = db.Column(db.String(200))
    documents     = db.Column(db.Text)  # liste des documents nécessaires
    etapes        = db.Column(db.Text)  # étapes à suivre
    duree         = db.Column(db.String(100))
    cout          = db.Column(db.String(100))
    telephone     = db.Column(db.String(20))
    adresse       = db.Column(db.String(300))
    formulaire    = db.Column(db.String(200))  # chemin fichier PDF
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)