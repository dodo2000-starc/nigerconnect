from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db
from models.news import Actualite

news_bp = Blueprint('news', __name__, url_prefix='/actualites')

CATEGORIES_NEWS = [
    'Info officielle', 'Alerte météo', 'Eau',
    'Électricité', 'Routes', 'Santé', 'Sécurité'
]

@news_bp.route('/')
def index():
    categorie = request.args.get('categorie', '')
    ville     = request.args.get('ville', '')
    page      = request.args.get('page', 1, type=int)

    query = Actualite.query.filter_by(est_publie=True)

    if categorie:
        query = query.filter_by(categorie=categorie)
    if ville:
        query = query.filter_by(ville=ville)

    # Alertes urgentes en tête
    query = query.order_by(
        Actualite.est_urgent.desc(),
        Actualite.date_creation.desc()
    )

    actualites = query.paginate(page=page, per_page=15, error_out=False)
    alertes    = Actualite.query.filter_by(
        est_urgent=True, est_publie=True
    ).order_by(Actualite.date_creation.desc()).limit(3).all()

    return render_template('news/index.html',
                           actualites=actualites,
                           alertes=alertes,
                           categories=CATEGORIES_NEWS,
                           categorie_active=categorie)

@news_bp.route('/<int:id>')
def detail(id):
    actu = Actualite.query.get_or_404(id)
    actu.nb_vues += 1
    db.session.commit()

    recentes = Actualite.query.filter(
        Actualite.id != id,
        Actualite.est_publie == True
    ).order_by(Actualite.date_creation.desc()).limit(5).all()

    return render_template('news/detail.html', actu=actu, recentes=recentes)

@news_bp.route('/publier', methods=['GET', 'POST'])
@login_required
def publier():
    # Seuls les admins peuvent publier
    if current_user.type_compte != 'admin':
        flash('Accès réservé aux administrateurs.', 'danger')
        return redirect(url_for('news.index'))

    if request.method == 'POST':
        actu = Actualite(
            titre      = request.form.get('titre'),
            contenu    = request.form.get('contenu'),
            categorie  = request.form.get('categorie'),
            ville      = request.form.get('ville'),
            est_urgent = bool(request.form.get('est_urgent')),
            auteur_id  = current_user.id,
        )
        db.session.add(actu)
        db.session.commit()
        flash('Actualité publiée !', 'success')
        return redirect(url_for('news.detail', id=actu.id))

    return render_template('news/publier.html',
                           categories=CATEGORIES_NEWS)