from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db
from models.annuaire import EntrepriseAnnuaire, AvisAnnuaire
from utils.helpers import CATEGORIES_ANNUAIRE, VILLES_NIGER

annuaire_bp = Blueprint('annuaire', __name__, url_prefix='/annuaire')

@annuaire_bp.route('/')
def index():
    categorie = request.args.get('categorie', '')
    ville     = request.args.get('ville', '')
    recherche = request.args.get('q', '')
    page      = request.args.get('page', 1, type=int)
    
    query = EntrepriseAnnuaire.query
    
    if categorie:
        query = query.filter_by(categorie=categorie)
    if ville:
        query = query.filter_by(ville=ville)
    if recherche:
        query = query.filter(
            EntrepriseAnnuaire.nom.ilike(f'%{recherche}%') |
            EntrepriseAnnuaire.description.ilike(f'%{recherche}%')
        )
    
    # Premium en premier
    query = query.order_by(
        EntrepriseAnnuaire.est_premium.desc(),
        EntrepriseAnnuaire.note_moyenne.desc()
    )
    
    entreprises = query.paginate(page=page, per_page=12, error_out=False)
    
    return render_template('annuaire/index.html',
                           entreprises=entreprises,
                           categories=CATEGORIES_ANNUAIRE,
                           villes=VILLES_NIGER,
                           categorie_active=categorie,
                           ville_active=ville,
                           recherche=recherche)

@annuaire_bp.route('/<int:id>')
def detail(id):
    entreprise = EntrepriseAnnuaire.query.get_or_404(id)
    entreprise.nb_vues += 1
    db.session.commit()
    
    avis = AvisAnnuaire.query.filter_by(
        entreprise_id=id
    ).order_by(AvisAnnuaire.date_creation.desc()).all()
    
    return render_template('annuaire/detail.html',
                           entreprise=entreprise,
                           avis=avis)

@annuaire_bp.route('/ajouter', methods=['GET', 'POST'])
@login_required
def ajouter():
    if request.method == 'POST':
        entreprise = EntrepriseAnnuaire(
            user_id    = current_user.id,
            nom        = request.form.get('nom'),
            categorie  = request.form.get('categorie'),
            description= request.form.get('description'),
            telephone  = request.form.get('telephone'),
            email      = request.form.get('email'),
            adresse    = request.form.get('adresse'),
            ville      = request.form.get('ville', 'Niamey'),
            quartier   = request.form.get('quartier'),
            horaires   = request.form.get('horaires'),
        )
        db.session.add(entreprise)
        db.session.commit()
        flash('Votre établissement a été ajouté à l\'annuaire !', 'success')
        return redirect(url_for('annuaire.detail', id=entreprise.id))
    
    return render_template('annuaire/ajouter.html',
                           categories=CATEGORIES_ANNUAIRE,
                           villes=VILLES_NIGER)

@annuaire_bp.route('/<int:id>/avis', methods=['POST'])
@login_required
def ajouter_avis(id):
    entreprise = EntrepriseAnnuaire.query.get_or_404(id)
    
    # Vérifier si l'utilisateur a déjà donné un avis
    avis_existant = AvisAnnuaire.query.filter_by(
        entreprise_id=id, user_id=current_user.id
    ).first()
    
    if avis_existant:
        flash('Vous avez déjà donné un avis pour cet établissement.', 'warning')
        return redirect(url_for('annuaire.detail', id=id))
    
    note        = request.form.get('note', type=int)
    commentaire = request.form.get('commentaire', '')
    
    if not note or note < 1 or note > 5:
        flash('Veuillez donner une note entre 1 et 5.', 'danger')
        return redirect(url_for('annuaire.detail', id=id))
    
    avis = AvisAnnuaire(
        entreprise_id=id,
        user_id=current_user.id,
        note=note,
        commentaire=commentaire
    )
    db.session.add(avis)
    
    # Recalculer la note moyenne
    tous_avis = AvisAnnuaire.query.filter_by(entreprise_id=id).all()
    total = sum(a.note for a in tous_avis) + note
    entreprise.note_moyenne = total / (len(tous_avis) + 1)
    
    db.session.commit()
    flash('Votre avis a été ajouté.', 'success')
    return redirect(url_for('annuaire.detail', id=id))