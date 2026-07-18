from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db
from models.job import OffreEmploi
from utils.helpers import VILLES_NIGER

jobs_bp = Blueprint('jobs', __name__, url_prefix='/emploi')

TYPES_CONTRAT = ['CDI', 'CDD', 'Stage', 'Freelance', 'Bénévolat']
SECTEURS = [
    'Agriculture', 'Commerce', 'Éducation', 'Santé', 'BTP',
    'Informatique', 'Finance', 'Transport', 'ONG', 'Administration', 'Autre'
]

@jobs_bp.route('/')
def index():
    secteur      = request.args.get('secteur', '')
    type_contrat = request.args.get('contrat', '')
    ville        = request.args.get('ville', '')
    recherche    = request.args.get('q', '')
    page         = request.args.get('page', 1, type=int)

    query = OffreEmploi.query.filter_by(est_actif=True)

    if secteur:
        query = query.filter_by(secteur=secteur)
    if type_contrat:
        query = query.filter_by(type_contrat=type_contrat)
    if ville:
        query = query.filter_by(ville=ville)
    if recherche:
        query = query.filter(
            OffreEmploi.titre.ilike(f'%{recherche}%') |
            OffreEmploi.description.ilike(f'%{recherche}%') |
            OffreEmploi.entreprise.ilike(f'%{recherche}%')
        )

    offres = query.order_by(
        OffreEmploi.date_creation.desc()
    ).paginate(page=page, per_page=10, error_out=False)

    return render_template('jobs/index.html',
                           offres=offres,
                           secteurs=SECTEURS,
                           types_contrat=TYPES_CONTRAT,
                           villes=VILLES_NIGER,
                           secteur_actif=secteur,
                           contrat_actif=type_contrat,
                           ville_active=ville,
                           recherche=recherche)

@jobs_bp.route('/<int:id>')
def detail(id):
    offre = OffreEmploi.query.get_or_404(id)
    offre.nb_vues += 1
    db.session.commit()

    similaires = OffreEmploi.query.filter(
        OffreEmploi.secteur == offre.secteur,
        OffreEmploi.id != id,
        OffreEmploi.est_actif == True
    ).limit(3).all()

    return render_template('jobs/detail.html',
                           offre=offre,
                           similaires=similaires)

@jobs_bp.route('/publier', methods=['GET', 'POST'])
@login_required
def publier():
    if request.method == 'POST':
        date_str = request.form.get('date_limite')
        date_limite = None
        if date_str:
            try:
                from datetime import datetime
                date_limite = datetime.strptime(date_str, '%Y-%m-%d')
            except ValueError:
                pass

        offre = OffreEmploi(
            recruteur_id  = current_user.id,
            titre         = request.form.get('titre'),
            entreprise    = request.form.get('entreprise'),
            description   = request.form.get('description'),
            type_contrat  = request.form.get('type_contrat'),
            secteur       = request.form.get('secteur'),
            ville         = request.form.get('ville', 'Niamey'),
            salaire_min   = float(request.form.get('salaire_min') or 0),
            salaire_max   = float(request.form.get('salaire_max') or 0),
            experience    = request.form.get('experience'),
            formation     = request.form.get('formation'),
            competences   = request.form.get('competences'),
            date_limite   = date_limite,
            telephone     = request.form.get('telephone',
                                             current_user.telephone),
            email_contact = request.form.get('email_contact',
                                             current_user.email),
        )
        db.session.add(offre)
        db.session.commit()
        flash('Offre d\'emploi publiée avec succès !', 'success')
        return redirect(url_for('jobs.detail', id=offre.id))

    return render_template('jobs/publier.html',
                           secteurs=SECTEURS,
                           types_contrat=TYPES_CONTRAT,
                           villes=VILLES_NIGER)

@jobs_bp.route('/<int:id>/fermer', methods=['POST'])
@login_required
def fermer(id):
    offre = OffreEmploi.query.get_or_404(id)
    if offre.recruteur_id != current_user.id:
        flash('Action non autorisée.', 'danger')
        return redirect(url_for('jobs.detail', id=id))
    offre.est_actif = False
    db.session.commit()
    flash('Offre d\'emploi fermée.', 'success')
    return redirect(url_for('jobs.index'))