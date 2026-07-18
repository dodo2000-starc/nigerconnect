from models import db
from datetime import datetime

class Transaction(db.Model):
    __tablename__ = 'transactions'
    
    id              = db.Column(db.Integer, primary_key=True)
    user_id         = db.Column(db.Integer, db.ForeignKey('users.id'))
    type_transaction = db.Column(db.String(100))
    # mobile_money | facture | service | taxe
    montant         = db.Column(db.Float, nullable=False)
    devise          = db.Column(db.String(10), default='FCFA')
    reference       = db.Column(db.String(100), unique=True)
    statut          = db.Column(db.String(50), default='en_attente')
    # en_attente | succes | echec | annule
    description     = db.Column(db.String(300))
    operateur       = db.Column(db.String(100))  # Orange | Airtel | Moov
    date_creation   = db.Column(db.DateTime, default=datetime.utcnow)
    date_traitement = db.Column(db.DateTime)