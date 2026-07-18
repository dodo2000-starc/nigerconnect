import os
import random
import string
from datetime import datetime
from werkzeug.utils import secure_filename
from flask import current_app

CATEGORIES_ANNUAIRE = [
    'Pharmacie', 'Hôtel', 'Restaurant', 'École', 'Garage',
    'Boutique', 'Service public', 'Banque', 'Hôpital', 'Autre'
]

CATEGORIES_MARKETPLACE = [
    'Immobilier', 'Véhicule', 'Agriculture', 'Électronique',
    'Mobilier', 'Vêtements', 'Matériel', 'Autre'
]

TYPES_SERVICE = [
    'Plombier', 'Électricien', 'Mécanicien', 'Informaticien',
    'Maçon', 'Soudeur', 'Couturier', 'Menuisier',
    'Peintre', 'Climatisation', 'Nettoyage', 'Autre'
]

VILLES_NIGER = [
    'Niamey', 'Zinder', 'Maradi', 'Tahoua', 'Agadez',
    'Dosso', 'Tillabéri', 'Diffa'
]

def generer_code_suivi():
    """Génère un code de suivi unique"""
    return 'NC' + ''.join(random.choices(string.digits, k=8))

def generer_reference():
    """Génère une référence de transaction"""
    return 'TXN' + datetime.now().strftime('%Y%m%d%H%M%S') + \
           ''.join(random.choices(string.digits, k=4))

def allowed_file(filename):
    """Vérifie si le fichier est autorisé"""
    allowed = current_app.config.get('ALLOWED_EXTENSIONS', {'png','jpg','jpeg','gif'})
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed

def save_file(file, subfolder='uploads'):
    """Sauvegarde un fichier uploadé"""
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Ajouter timestamp pour unicité
        name, ext = os.path.splitext(filename)
        filename = f"{name}_{datetime.now().strftime('%Y%m%d%H%M%S')}{ext}"
        upload_path = os.path.join(current_app.root_path, 'static', subfolder)
        os.makedirs(upload_path, exist_ok=True)
        file.save(os.path.join(upload_path, filename))
        return f"static/{subfolder}/{filename}"
    return None

def formater_prix(montant):
    """Formate un prix en FCFA"""
    if montant is None:
        return "Prix non défini"
    return f"{int(montant):,} FCFA".replace(',', ' ')

def temps_ecoule(date):
    """Retourne le temps écoulé depuis une date"""
    if not date:
        return ""
    delta = datetime.utcnow() - date
    if delta.days > 30:
        return date.strftime('%d/%m/%Y')
    elif delta.days > 0:
        return f"il y a {delta.days} jour(s)"
    elif delta.seconds > 3600:
        return f"il y a {delta.seconds // 3600}h"
    elif delta.seconds > 60:
        return f"il y a {delta.seconds // 60} min"
    else:
        return "à l'instant"