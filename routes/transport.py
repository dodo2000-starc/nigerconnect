from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db
from models.transport import Trajet, Livraison
from utils.helpers import VILLES_NIGER, generer_code_suivi
from datetime import datetime

transport_bp = Blueprint('transport', __name__, url_prefix='/transport')

@transport_bp.route('/')
def index():
    depart      = request.args.get('depart', '')
    destination = request.args.get('destination', '')
    date        = request.args.get('date', '')
    page        = request.args.get('page', 1, type=int)

    query = Trajet.query.filter_by(est_actif=True)

    if depart:
        query = query.filter(Trajet.depart.ilike(f'%{depart}%'))
    if destination:
        query = query.filter(Trajet.destination.ilike(f'%{destination}%'))
    if date:
        try:
            date_obj = datetime.strptime(date, '%Y-%m-%d')
            query = query.filter(
                db.func.date(Trajet.date_depart) == date_obj.date()
            )
        except ValueError:
            pass

    trajets = query.order_by(Trajet.date_depart.asc()).paginate(
        page=page, per_page=10, error_out=False
    )

    return render_template('transport/index.html',
                           trajets=trajets,
                           villes=VILLES_NIGER,
                           depart=depart,
                           destination=destination,
                           date=date)

@transport_bp.route('/ajouter-trajet', methods=['GET', 'POST'])
@login_required
def ajouter_trajet():
    if request.method == 'POST':
        date_str = request.form.get('date_depart')
        try:
            date_depart = datetime.strptime(date_str, '%Y-%m-%dT%H:%M')
        except ValueError:
            flash('Format de date invalide.', 'danger')
            return render_template('transport/ajouter_trajet.html',
                                   villes=VILLES_NIGER)

        trajet = Trajet(
            compagnie      = request.form.get('compagnie'),
            type_transport = request.form.get('type_transport', 'bus'),
            depart         = request.form.get('depart'),
            destination    = request.form.get('destination'),
            date_depart    = date_depart,
            places_total   = int(request.form.get('places_total', 0)),
            places_dispo   = int(request.form.get('places_total', 0)),
            prix           = float(request.form.get('prix', 0)),
            telephone      = request.form.get('telephone',
                                              current_user.telephone),
        )
        db.session.add(trajet)
        db.session.commit()
        flash('Trajet ajouté avec succès !', 'success')
        return redirect(url_for('transport.index'))

    return render_template('transport/ajouter_trajet.html',
                           villes=VILLES_NIGER)

@transport_bp.route('/livraison', methods=['GET', 'POST'])
@login_required
def livraison():
    if request.method == 'POST':
        code = generer_code_suivi()
        liv  = Livraison(
            expediteur_id   = current_user.id,
            description     = request.form.get('description'),
            adresse_depart  = request.form.get('adresse_depart'),
            adresse_arrivee = request.form.get('adresse_arrivee'),
            poids           = float(request.form.get('poids') or 0),
            prix            = float(request.form.get('prix') or 0),
            code_suivi      = code,
        )
        db.session.add(liv)
        db.session.commit()
        flash(f'Livraison créée ! Code de suivi : {code}', 'success')
        return redirect(url_for('transport.suivi', code=code))

    return render_template('transport/livraison.html')

@transport_bp.route('/suivi')
def suivi():
    code     = request.args.get('code', '')
    livraison = None
    if code:
        livraison = Livraison.query.filter_by(code_suivi=code).first()
        if not livraison:
            flash('Code de suivi introuvable.', 'danger')

    return render_template('transport/suivi.html',
                           livraison=livraison,
                           code=code)