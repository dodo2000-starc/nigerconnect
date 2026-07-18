from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db
from models.health import EtablissementSante, RendezVousSante
from utils.helpers import VILLES_NIGER
from datetime import datetime

health_bp = Blueprint('health', __name__, url_prefix='/sante')

TYPES_ETAB = ['hôpital', 'clinique', 'pharmacie', 'cabinet']

@health_bp.route('/')
def index():
    type_etab = request.args.get('type', '')
    ville     = request.args.get('ville', '')
    urgences  = request.args.get('urgences', '')
    recherche = request.args.get('q', '')
    page      = request.args.get('page', 1, type=int)

    query = EtablissementSante.query.filter_by(est_actif=True)

    if type_etab:
        query = query.filter_by(type_etab=type_etab)
    if ville:
        query = query.filter_by(ville=ville)
    if urgences:
        query = query.filter_by(urgences=True)
    if recherche:
        query = query.filter(
            EtablissementSante.nom.ilike(f'%{recherche}%') |
            EtablissementSante.quartier.ilike(f'%{recherche}%')
        )

    etablissements = query.paginate(page=page, per_page=12, error_out=False)

    return render_template('health/index.html',
                           etablissements=etablissements,
                           types_etab=TYPES_ETAB,
                           villes=VILLES_NIGER,
                           type_actif=type_etab,
                           ville_active=ville)

@health_bp.route('/<int:id>')
def detail(id):
    etab = EtablissementSante.query.get_or_404(id)
    rdvs = []
    if current_user.is_authenticated:
        rdvs = RendezVousSante.query.filter_by(
            user_id=current_user.id,
            etablissement_id=id
        ).order_by(RendezVousSante.date_rdv.desc()).all()

    return render_template('health/detail.html', etab=etab, rdvs=rdvs)

@health_bp.route('/<int:id>/rdv', methods=['POST'])
@login_required
def prendre_rdv(id):
    etab    = EtablissementSante.query.get_or_404(id)
    date_str = request.form.get('date_rdv')
    motif   = request.form.get('motif')

    try:
        date_rdv = datetime.strptime(date_str, '%Y-%m-%dT%H:%M')
    except ValueError:
        flash('Format de date invalide.', 'danger')
        return redirect(url_for('health.detail', id=id))

    rdv = RendezVousSante(
        user_id          = current_user.id,
        etablissement_id = id,
        motif            = motif,
        date_rdv         = date_rdv,
    )
    db.session.add(rdv)
    db.session.commit()
    flash(f'Rendez-vous pris le {date_rdv.strftime("%d/%m/%Y à %H:%M")}.', 'success')
    return redirect(url_for('health.detail', id=id))

@health_bp.route('/mes-rdv')
@login_required
def mes_rdv():
    rdvs = RendezVousSante.query.filter_by(
        user_id=current_user.id
    ).order_by(RendezVousSante.date_rdv.desc()).all()
    return render_template('health/mes_rdv.html', rdvs=rdvs)