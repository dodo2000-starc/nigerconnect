from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db
from models.marketplace import Annonce
from utils.helpers import CATEGORIES_MARKETPLACE, VILLES_NIGER
import json

marketplace_bp = Blueprint('marketplace', __name__, url_prefix='/marche')

@marketplace_bp.route('/')
def index():
    categorie = request.args.get('categorie', '')
    ville     = request.args.get('ville', '')
    recherche = request.args.get('q', '')
    prix_max  = request.args.get('prix_max', type=float)
    page      = request.args.get('page', 1, type=int)
    
    query = Annonce.query.filter_by(statut='active')
    
    if categorie:
        query = query.filter_by(categorie=categorie)
    if ville:
        query = query.filter_by(ville=ville)
    if recherche:
        query = query.filter(
            Annonce.titre.ilike(f'%{recherche}%') |
            Annonce.description.ilike(f'%{recherche}%')
        )
    if prix_max:
        query = query.filter(Annonce.prix <= prix_max)
    
    query = query.order_by(
        Annonce.est_premium.desc(),
        Annonce.date_creation.desc()
    )
    
    annonces = query.paginate(page=page, per_page=12, error_out=False)
    
    return render_template('marketplace/index.html',
                           annonces=annonces,
                           categories=CATEGORIES_MARKETPLACE,
                           villes=VILLES_NIGER,
                           categorie_active=categorie,
                           ville_active=ville,
                           recherche=recherche)

@marketplace_bp.route('/<int:id>')
def detail(id):
    annonce = Annonce.query.get_or_404(id)
    annonce.nb_vues += 1
    db.session.commit()
    
    # Annonces similaires
    similaires = Annonce.query.filter(
        Annonce.categorie == annonce.categorie,
        Annonce.id != id,
        Annonce.statut == 'active'
    ).limit(4).all()
    
    images = []
    if annonce.images:
        try:
            images = json.loads(annonce.images)
        except Exception:
            images = []
    
    return render_template('marketplace/detail.html',
                           annonce=annonce,
                           similaires=similaires,
                           images=images)

@marketplace_bp.route('/publier', methods=['GET', 'POST'])
@login_required
def publier():
    if request.method == 'POST':
        annonce = Annonce(
            user_id       = current_user.id,
            titre         = request.form.get('titre'),
            description   = request.form.get('description'),
            prix          = float(request.form.get('prix', 0)),
            prix_negociable = bool(request.form.get('prix_negociable')),
            categorie     = request.form.get('categorie'),
            etat          = request.form.get('etat', 'Neuf'),
            ville         = request.form.get('ville', 'Niamey'),
            quartier      = request.form.get('quartier'),
            telephone     = request.form.get('telephone',
                                             current_user.telephone),
        )
        db.session.add(annonce)
        db.session.commit()
        flash('Votre annonce a été publiée !', 'success')
        return redirect(url_for('marketplace.detail', id=annonce.id))
    
    return render_template('marketplace/publier.html',
                           categories=CATEGORIES_MARKETPLACE,
                           villes=VILLES_NIGER)

@marketplace_bp.route('/<int:id>/marquer-vendu', methods=['POST'])
@login_required
def marquer_vendu(id):
    annonce = Annonce.query.get_or_404(id)
    if annonce.user_id != current_user.id:
        flash('Action non autorisée.', 'danger')
        return redirect(url_for('marketplace.detail', id=id))
    
    annonce.statut = 'vendu'
    db.session.commit()
    flash('Annonce marquée comme vendue.', 'success')
    return redirect(url_for('marketplace.index'))