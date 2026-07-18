from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db
from models.agriculture import PrixMarche, AnnonceAgricole
from utils.helpers import VILLES_NIGER

agriculture_bp = Blueprint('agriculture', __name__, url_prefix='/agriculture')

CATEGORIES_AGRI = ['céréales', 'légumineuses', 'légumes', 'fruits',
                   'bétail', 'volaille', 'intrants', 'matériel']

@agriculture_bp.route('/')
def index():
    prix = PrixMarche.query.order_by(
        PrixMarche.date_releve.desc()
    ).all()

    annonces = AnnonceAgricole.query.filter_by(
        est_actif=True
    ).order_by(AnnonceAgricole.date_creation.desc()).limit(8).all()

    return render_template('agriculture/index.html',
                           prix=prix,
                           annonces=annonces,
                           categories=CATEGORIES_AGRI,
                           villes=VILLES_NIGER)

@agriculture_bp.route('/prix')
def prix_marche():
    categorie = request.args.get('categorie', '')
    ville     = request.args.get('ville', '')
    produit   = request.args.get('produit', '')

    query = PrixMarche.query

    if categorie:
        query = query.filter_by(categorie=categorie)
    if ville:
        query = query.filter_by(ville=ville)
    if produit:
        query = query.filter(PrixMarche.produit.ilike(f'%{produit}%'))

    prix = query.order_by(
        PrixMarche.date_releve.desc()
    ).all()

    return render_template('agriculture/prix.html',
                           prix=prix,
                           categories=CATEGORIES_AGRI,
                           villes=VILLES_NIGER,
                           categorie_active=categorie,
                           ville_active=ville)

@agriculture_bp.route('/annonces')
def annonces():
    type_annonce = request.args.get('type', '')
    page         = request.args.get('page', 1, type=int)

    query = AnnonceAgricole.query.filter_by(est_actif=True)

    if type_annonce:
        query = query.filter_by(type_annonce=type_annonce)

    annonces = query.order_by(
        AnnonceAgricole.date_creation.desc()
    ).paginate(page=page, per_page=12, error_out=False)

    return render_template('agriculture/annonces.html',
                           annonces=annonces,
                           type_actif=type_annonce)

@agriculture_bp.route('/publier', methods=['GET', 'POST'])
@login_required
def publier():
    if request.method == 'POST':
        annonce = AnnonceAgricole(
            user_id      = current_user.id,
            type_annonce = request.form.get('type_annonce'),
            produit      = request.form.get('produit'),
            quantite     = float(request.form.get('quantite') or 0),
            unite        = request.form.get('unite'),
            prix         = float(request.form.get('prix') or 0),
            description  = request.form.get('description'),
            ville        = request.form.get('ville', 'Niamey'),
            telephone    = request.form.get('telephone',
                                            current_user.telephone),
        )
        db.session.add(annonce)
        db.session.commit()
        flash('Annonce agricole publiée !', 'success')
        return redirect(url_for('agriculture.annonces'))

    return render_template('agriculture/publier.html',
                           villes=VILLES_NIGER)