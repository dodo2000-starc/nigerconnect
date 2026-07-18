from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models.annuaire import EntrepriseAnnuaire
from models.marketplace import Annonce
from models.service import Prestataire
from models.news import Actualite
from models.agriculture import PrixMarche
from models.job import OffreEmploi
from models.health import EtablissementSante

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@dashboard_bp.route('/')
@login_required
def index():
    # Statistiques
    stats = {
        'entreprises': EntrepriseAnnuaire.query.filter_by(est_verifie=True).count(),
        'annonces': Annonce.query.filter_by(statut='active').count(),
        'prestataires': Prestataire.query.filter_by(disponible=True).count(),
        'offres_emploi': OffreEmploi.query.filter_by(est_actif=True).count(),
    }
    
    # Actualités urgentes
    alertes = Actualite.query.filter_by(
        est_urgent=True, est_publie=True
    ).order_by(Actualite.date_creation.desc()).limit(3).all()
    
    # Dernières annonces
    annonces = Annonce.query.filter_by(
        statut='active'
    ).order_by(Annonce.date_creation.desc()).limit(6).all()
    
    # Prix du marché
    prix = PrixMarche.query.order_by(
        PrixMarche.date_releve.desc()
    ).limit(6).all()
    
    return render_template('dashboard/index.html',
                           stats=stats,
                           alertes=alertes,
                           annonces=annonces,
                           prix=prix)