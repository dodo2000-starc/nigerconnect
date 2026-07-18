from models import db
from datetime import datetime

class PrixMarche(db.Model):
    __tablename__ = 'prix_marche'
    
    id          = db.Column(db.Integer, primary_key=True)
    produit     = db.Column(db.String(150), nullable=False)
    categorie   = db.Column(db.String(100))  # céréales | légumes | fruits | bétail
    prix_min    = db.Column(db.Float)
    prix_max    = db.Column(db.Float)
    unite       = db.Column(db.String(50))  # kg | sac | tête
    marche      = db.Column(db.String(150))
    ville       = db.Column(db.String(100))
    date_releve = db.Column(db.DateTime, default=datetime.utcnow)

class AnnonceAgricole(db.Model):
    __tablename__ = 'annonces_agricoles'
    
    id            = db.Column(db.Integer, primary_key=True)
    user_id       = db.Column(db.Integer, db.ForeignKey('users.id'))
    type_annonce  = db.Column(db.String(50))  # vente | achat | location
    produit       = db.Column(db.String(150), nullable=False)
    quantite      = db.Column(db.Float)
    unite         = db.Column(db.String(50))
    prix          = db.Column(db.Float)
    description   = db.Column(db.Text)
    ville         = db.Column(db.String(100))
    telephone     = db.Column(db.String(20))
    est_actif     = db.Column(db.Boolean, default=True)
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)