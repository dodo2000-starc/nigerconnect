from models import db
from datetime import datetime

class Actualite(db.Model):
    __tablename__ = 'actualites'
    
    id            = db.Column(db.Integer, primary_key=True)
    titre         = db.Column(db.String(300), nullable=False)
    contenu       = db.Column(db.Text, nullable=False)
    categorie     = db.Column(db.String(100))
    # Info officielle | Alerte météo | Eau | Électricité | Routes | Santé
    ville         = db.Column(db.String(100))
    est_urgent    = db.Column(db.Boolean, default=False)
    auteur_id     = db.Column(db.Integer, db.ForeignKey('users.id'))
    image         = db.Column(db.String(200))
    nb_vues       = db.Column(db.Integer, default=0)
    est_publie    = db.Column(db.Boolean, default=True)
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)