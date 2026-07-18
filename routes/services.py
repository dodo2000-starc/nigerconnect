from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db
from models.service import Prestataire, DemandeService
from utils.helpers import TYPES_SERVICE, VILLES_NIGER

services_bp = Blueprint('services', __name__, url_prefix='/services')

@services_bp.route('/')
def index():
    service_type = request.args.get('type', '')
    ville        = request.args.get('ville', '')
    page         = request.args.get('page', 1, type=int)
    
    query = Prestataire.query.filter_by(disponible=True)
    
    if service_type:
        query = query.filter_by(service_type=service_type)
    if ville:
        query = query.filter_by(ville=ville)
    
    query = query.order_by(
        Prestataire.est_verifie.desc(),
        Prestataire.note_moyenne.desc()
    )
    
    prestataires = query.paginate(page=page, per_page=12, error_out=False)
    
    return render_template('services/index.html',
                           prestataires=prestataires,
                           types_service=TYPES_SERVICE,
                           villes=VILLES_NIGER,
                           type_actif=service_type,
                           ville_active=ville)

@services_bp.route('/<int:id>')
def detail(id):
    prestataire = Prestataire.query.get_or_404(id)
    return render_template('services/detail.html', prestataire=prestataire)

@services_bp.route('/inscription', methods=['GET', 'POST'])
@login_required
def inscription():
    # Vérifier si déjà prestataire
    existant = Prestataire.query.filter_by(user_id=current_user.id).first()
    
    if request.method == 'POST':
        if existant:
            # Mettre à jour
            existant.service_type     = request.form.get('service_type')
            existant.specialites      = request.form.get('specialites')
            existant.description      = request.form.get('description')
            existant.experience_years = int(request.form.get('experience_years', 0))
            existant.tarif_min        = float(request.form.get('tarif_min') or 0)
            existant.tarif_max        = float(request.form.get('tarif_max') or 0)
            existant.ville            = request.form.get('ville', 'Niamey')
            existant.quartier         = request.form.get('quartier')
            existant.telephone        = request.form.get('telephone',
                                                         current_user.telephone)
            db.session.commit()
            flash('Votre profil prestataire a été mis à jour.', 'success')
        else:
            prestataire = Prestataire(
                user_id          = current_user.id,
                service_type     = request.form.get('service_type'),
                specialites      = request.form.get('specialites'),
                description      = request.form.get('description'),
                experience_years = int(request.form.get('experience_years', 0)),
                tarif_min        = float(request.form.get('tarif_min') or 0),
                tarif_max        = float(request.form.get('tarif_max') or 0),
                ville            = request.form.get('ville', 'Niamey'),
                quartier         = request.form.get('quartier'),
                telephone        = request.form.get('telephone',
                                                    current_user.telephone),
            )
            db.session.add(prestataire)
            db.session.commit()
            flash('Félicitations ! Vous êtes maintenant prestataire.', 'success')
        
        return redirect(url_for('services.index'))
    
    return render_template('services/inscription.html',
                           types_service=TYPES_SERVICE,
                           villes=VILLES_NIGER,
                           prestataire=existant)

@services_bp.route('/demande/<int:prestataire_id>', methods=['POST'])
@login_required
def demander(prestataire_id):
    prestataire = Prestataire.query.get_or_404(prestataire_id)
    
    demande = DemandeService(
        client_id      = current_user.id,
        prestataire_id = prestataire_id,
        description    = request.form.get('description'),
        adresse        = request.form.get('adresse'),
        budget         = float(request.form.get('budget') or 0),
    )
    db.session.add(demande)
    db.session.commit()
    flash('Votre demande a été envoyée au prestataire.', 'success')
    return redirect(url_for('services.detail', id=prestataire_id))