from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, login_required, current_user
from models import db
from models.user import User
from datetime import datetime

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/inscription', methods=['GET', 'POST'])
def inscription():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    
    if request.method == 'POST':
        nom       = request.form.get('nom', '').strip()
        prenom    = request.form.get('prenom', '').strip()
        telephone = request.form.get('telephone', '').strip()
        email     = request.form.get('email', '').strip()
        password  = request.form.get('password', '')
        confirm   = request.form.get('confirm_password', '')
        type_compte = request.form.get('type_compte', 'citoyen')
        ville     = request.form.get('ville', 'Niamey')
        
        # Validations
        if not all([nom, prenom, telephone, password]):
            flash('Veuillez remplir tous les champs obligatoires.', 'danger')
            return render_template('auth/inscription.html')
        
        if password != confirm:
            flash('Les mots de passe ne correspondent pas.', 'danger')
            return render_template('auth/inscription.html')
        
        if len(password) < 6:
            flash('Le mot de passe doit contenir au moins 6 caractères.', 'danger')
            return render_template('auth/inscription.html')
        
        if User.query.filter_by(telephone=telephone).first():
            flash('Ce numéro de téléphone est déjà utilisé.', 'danger')
            return render_template('auth/inscription.html')
        
        if email and User.query.filter_by(email=email).first():
            flash('Cet email est déjà utilisé.', 'danger')
            return render_template('auth/inscription.html')
        
        # Créer l'utilisateur
        user = User(
            nom=nom,
            prenom=prenom,
            telephone=telephone,
            email=email if email else None,
            type_compte=type_compte,
            ville=ville
        )
        user.set_password(password)
        
        try:
            db.session.add(user)
            db.session.commit()
            login_user(user)
            flash(f'Bienvenue {user.prenom} ! Votre compte a été créé.', 'success')
            return redirect(url_for('dashboard.index'))
        except Exception as e:
            db.session.rollback()
            flash('Erreur lors de la création du compte.', 'danger')
    
    return render_template('auth/inscription.html')

@auth_bp.route('/connexion', methods=['GET', 'POST'])
def connexion():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    
    if request.method == 'POST':
        telephone = request.form.get('telephone', '').strip()
        password  = request.form.get('password', '')
        remember  = request.form.get('remember', False)
        
        user = User.query.filter_by(telephone=telephone).first()
        
        if user and user.check_password(password):
            if not user.is_active:
                flash('Votre compte a été suspendu.', 'danger')
                return render_template('auth/connexion.html')
            
            user.derniere_connexion = datetime.utcnow()
            db.session.commit()
            login_user(user, remember=bool(remember))
            
            next_page = request.args.get('next')
            flash(f'Bienvenue {user.prenom} !', 'success')
            return redirect(next_page or url_for('dashboard.index'))
        else:
            flash('Numéro de téléphone ou mot de passe incorrect.', 'danger')
    
    return render_template('auth/connexion.html')

@auth_bp.route('/deconnexion')
@login_required
def deconnexion():
    logout_user()
    flash('Vous avez été déconnecté.', 'info')
    return redirect(url_for('main.index'))

@auth_bp.route('/profil', methods=['GET', 'POST'])
@login_required
def profil():
    if request.method == 'POST':
        current_user.nom     = request.form.get('nom', current_user.nom)
        current_user.prenom  = request.form.get('prenom', current_user.prenom)
        current_user.email   = request.form.get('email', current_user.email)
        current_user.ville   = request.form.get('ville', current_user.ville)
        current_user.quartier = request.form.get('quartier', current_user.quartier)
        
        new_password = request.form.get('new_password', '')
        if new_password:
            if len(new_password) >= 6:
                current_user.set_password(new_password)
            else:
                flash('Le nouveau mot de passe doit avoir au moins 6 caractères.', 'danger')
                return render_template('auth/profil.html')
        
        db.session.commit()
        flash('Profil mis à jour avec succès.', 'success')
    
    return render_template('auth/profil.html')