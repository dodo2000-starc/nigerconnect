"""
Script pour peupler la base de données avec du contenu réel du Niger.
Usage : python seed_data.py
"""

from app import app, db
from models.user import User
from models.annuaire import EntrepriseAnnuaire
from models.marketplace import Annonce
from models.service import Prestataire
from models.job import OffreEmploi
from models.agriculture import AnnonceAgricole, PrixMarche
from models.health import EtablissementSante
from models.news import Actualite
from models.admin_service import DemarcheAdmin
from datetime import datetime, timedelta
import random

def creer_utilisateurs_demo():
    """Créer des utilisateurs de démonstration"""
    utilisateurs = [
        ('Ibrahim', 'Moussa',    '90111111', 'entreprise', 'Niamey'),
        ('Fatima',  'Abdou',     '90222222', 'entreprise', 'Niamey'),
        ('Adamou',  'Hassane',   '90333333', 'artisan',    'Niamey'),
        ('Zeinab',  'Souley',    '90444444', 'artisan',    'Niamey'),
        ('Ali',     'Garba',     '90555555', 'artisan',    'Zinder'),
        ('Aïcha',   'Ousmane',   '90666666', 'citoyen',    'Niamey'),
        ('Mahamadou','Issoufou', '90777777', 'entreprise', 'Maradi'),
        ('Rakia',   'Amadou',    '90888888', 'artisan',    'Tahoua'),
        ('Salif',   'Boubacar',  '90999999', 'entreprise', 'Niamey'),
        ('Hadiza',  'Idrissa',   '91111111', 'citoyen',    'Niamey'),
    ]

    users_crees = []
    for prenom, nom, tel, type_c, ville in utilisateurs:
        existant = User.query.filter_by(telephone=tel).first()
        if not existant:
            user = User(
                nom=nom, prenom=prenom, telephone=tel,
                type_compte=type_c, ville=ville,
                is_verified=True, is_active=True
            )
            user.set_password('Password123!')
            db.session.add(user)
            users_crees.append(user)
        else:
            users_crees.append(existant)

    db.session.commit()
    print(f"✅ {len(users_crees)} utilisateurs prêts")
    return users_crees

def creer_entreprises_annuaire(users):
    """Ajouter des entreprises réelles de Niamey"""
    if EntrepriseAnnuaire.query.count() > 5:
        print("⏭️  Entreprises déjà présentes")
        return

    entreprises = [
        # Pharmacies
        ('Pharmacie Populaire', 'Pharmacie', 'Pharmacie de garde 24h/24',
         '+227 20 73 45 12', 'Avenue de la Liberté', 'Niamey', 'Plateau',
         '24h/24 - 7j/7', True, True),
        ('Pharmacie de la Paix', 'Pharmacie', 'Large gamme de médicaments',
         '+227 20 74 22 33', 'Rond-point Kennedy', 'Niamey', 'Yantala',
         '7h-22h', True, False),
        ('Pharmacie du Grand Marché', 'Pharmacie', 'Au cœur du marché central',
         '+227 20 73 15 66', 'Grand Marché', 'Niamey', 'Grand Marché',
         '7h-21h', True, False),

        # Hôtels
        ('Hôtel Gaweye', 'Hôtel', 'Hôtel 4 étoiles au bord du fleuve Niger',
         '+227 20 72 27 30', 'Bord du fleuve', 'Niamey', 'Plateau',
         '24h/24', True, True),
        ('Grand Hôtel de Niamey', 'Hôtel', 'Hôtel historique de Niamey',
         '+227 20 73 26 41', 'Rue du Sahel', 'Niamey', 'Plateau',
         '24h/24', True, True),
        ('Hôtel Terminus', 'Hôtel', 'Hôtel confortable centre-ville',
         '+227 20 73 26 92', 'Avenue de la République', 'Niamey', 'Terminus',
         '24h/24', True, False),

        # Restaurants
        ('Restaurant Le Pilier', 'Restaurant', 'Cuisine nigérienne et internationale',
         '+227 20 73 45 78', 'Route de Tillabéri', 'Niamey', 'Plateau',
         '11h-23h', True, False),
        ('Le Diamangou', 'Restaurant', 'Spécialités locales - Riz au gras, mafé',
         '+227 96 12 34 56', 'Corniche Yantala', 'Niamey', 'Yantala',
         '10h-22h', True, False),
        ('Restaurant Chez Tantie', 'Restaurant', 'Cuisine familiale nigérienne',
         '+227 90 55 66 77', 'Quartier Kalley', 'Niamey', 'Kalley',
         '7h-22h', False, False),

        # Écoles
        ('École Française Jean de La Fontaine', 'École',
         'Enseignement français de la maternelle au lycée',
         '+227 20 72 22 40', 'Plateau', 'Niamey', 'Plateau',
         'Lun-Ven 7h-17h', True, False),
        ('Université Abdou Moumouni', 'École',
         'Principale université publique du Niger',
         '+227 20 31 52 37', 'Route de Torodi', 'Niamey', 'Université',
         'Lun-Ven 7h-18h', True, False),

        # Garages
        ('Garage Auto Niger', 'Garage', 'Réparation toutes marques',
         '+227 96 45 78 12', 'Route de Say', 'Niamey', 'Lazaret',
         'Lun-Sam 7h-19h', True, False),
        ('Garage Moderne', 'Garage', 'Spécialiste diagnostic électronique',
         '+227 90 22 33 44', 'Rond-point 6ème', 'Niamey', '6ème arrondissement',
         'Lun-Sam 8h-18h', True, False),

        # Banques
        ('Bank Of Africa Niger', 'Banque', 'Services bancaires et Mobile Banking',
         '+227 20 73 36 20', 'Avenue de la Mairie', 'Niamey', 'Plateau',
         'Lun-Ven 8h-16h', True, True),
        ('Ecobank Niger', 'Banque', 'Banque panafricaine',
         '+227 20 73 71 81', 'Rue des Bâtisseurs', 'Niamey', 'Plateau',
         'Lun-Ven 8h-16h', True, True),

        # Boutiques
        ('Orange Store Plateau', 'Boutique', 'Téléphones, forfaits et Orange Money',
         '+227 91 00 00 00', 'Rue du Commerce', 'Niamey', 'Plateau',
         'Lun-Sam 8h-20h', True, True),
        ('Airtel Shop', 'Boutique', 'Services Airtel et Airtel Money',
         '+227 97 00 00 00', 'Grand Marché', 'Niamey', 'Grand Marché',
         'Lun-Sam 8h-20h', True, False),

        # Services publics
        ('Mairie Centrale de Niamey', 'Service public',
         'État civil, cartes d\'identité, actes de naissance',
         '+227 20 72 20 15', 'Place de la République', 'Niamey', 'Plateau',
         'Lun-Ven 7h30-15h30', True, False),
        ('Poste Centrale', 'Service public',
         'Courrier, colis, mandats',
         '+227 20 73 34 45', 'Rue de la Poste', 'Niamey', 'Plateau',
         'Lun-Ven 7h30-16h', True, False),

        # Hôpital
        ('Hôpital National de Niamey', 'Hôpital',
         'Principal hôpital de référence du Niger',
         '+227 20 72 25 20', 'Avenue de l\'Hôpital', 'Niamey', 'Plateau',
         '24h/24 - Urgences', True, True),
    ]

    for i, e in enumerate(entreprises):
        nom, cat, desc, tel, adresse, ville, quartier, horaires, verifie, premium = e
        user = users[i % len(users)]

        entreprise = EntrepriseAnnuaire(
            user_id=user.id,
            nom=nom,
            categorie=cat,
            description=desc,
            telephone=tel,
            adresse=adresse,
            ville=ville,
            quartier=quartier,
            horaires=horaires,
            est_verifie=verifie,
            est_premium=premium,
            note_moyenne=round(random.uniform(3.5, 5.0), 1),
            nb_vues=random.randint(15, 500)
        )
        db.session.add(entreprise)

    db.session.commit()
    print(f"✅ {len(entreprises)} entreprises ajoutées à l'annuaire")

def creer_annonces_marketplace(users):
    """Ajouter des annonces au marché"""
    if Annonce.query.count() > 5:
        print("⏭️  Annonces déjà présentes")
        return

    annonces = [
        # Véhicules
        ('Toyota Corolla 2018 en excellent état',
         'Voiture bien entretenue, climatisation, kilométrage 65 000 km. Vidange à jour, pneus neufs.',
         4500000, 'Véhicule', 'Bon état', 'Niamey', 'Plateau'),
        ('Moto Yamaha DT 125 - 2020',
         'Moto tout-terrain, idéale pour la ville et la brousse. Peu utilisée.',
         850000, 'Véhicule', 'Bon état', 'Niamey', 'Yantala'),
        ('Peugeot 206 - Occasion',
         'Voiture citadine économique, parfaite pour Niamey.',
         2100000, 'Véhicule', 'Usage', 'Niamey', 'Kalley'),

        # Immobilier
        ('Villa moderne 4 chambres à Yantala',
         'Belle villa avec cour, garage, jardin. 4 chambres, 2 salons, cuisine équipée.',
         85000000, 'Immobilier', 'Neuf', 'Niamey', 'Yantala'),
        ('Terrain 500m² à Cité Chinoise',
         'Terrain viabilisé, titre foncier, quartier calme et sécurisé.',
         25000000, 'Immobilier', 'Neuf', 'Niamey', 'Cité Chinoise'),
        ('Appartement 3 pièces à louer - Plateau',
         'Appartement meublé, climatisé, situé au cœur du Plateau. 350 000 FCFA/mois.',
         350000, 'Immobilier', 'Bon état', 'Niamey', 'Plateau'),

        # Électronique
        ('iPhone 13 Pro Max 256Go',
         'Téléphone comme neuf, dans sa boîte avec tous les accessoires.',
         550000, 'Électronique', 'Bon état', 'Niamey', 'Plateau'),
        ('Ordinateur portable HP Pavilion',
         'Core i5, 8Go RAM, 512Go SSD. Idéal pour étudiants et professionnels.',
         425000, 'Électronique', 'Bon état', 'Niamey', 'Terminus'),
        ('Samsung Galaxy A54 - Neuf',
         'Téléphone neuf sous garantie, 128Go, double SIM.',
         285000, 'Électronique', 'Neuf', 'Niamey', 'Grand Marché'),
        ('TV LED Samsung 55 pouces',
         'Smart TV 4K, WiFi intégré, télécommande incluse.',
         320000, 'Électronique', 'Bon état', 'Niamey', 'Plateau'),

        # Mobilier
        ('Salon complet 7 places en cuir',
         'Salon élégant en cuir véritable, très peu utilisé. Livraison possible.',
         850000, 'Mobilier', 'Bon état', 'Niamey', 'Yantala'),
        ('Lit king size avec matelas',
         'Lit en bois massif avec matelas orthopédique neuf.',
         180000, 'Mobilier', 'Bon état', 'Niamey', 'Kalley'),

        # Agriculture
        ('Sacs de mil - 100 sacs disponibles',
         'Mil de première qualité, récolte 2024. Prix dégressif selon quantité.',
         22000, 'Agriculture', 'Neuf', 'Maradi', 'Marché central'),
        ('Motopompe agricole neuve',
         'Motopompe Honda 6.5 CV, idéale pour irrigation. Garantie 1 an.',
         285000, 'Agriculture', 'Neuf', 'Tahoua', 'Centre-ville'),

        # Matériel
        ('Groupe électrogène 5 KVA',
         'Groupe électrogène silencieux, essence. Parfait état de fonctionnement.',
         450000, 'Matériel', 'Bon état', 'Niamey', 'Route de Say'),
    ]

    for titre, desc, prix, cat, etat, ville, quartier in annonces:
        user = random.choice(users)
        annonce = Annonce(
            user_id=user.id,
            titre=titre,
            description=desc,
            prix=prix,
            prix_negociable=random.choice([True, False]),
            categorie=cat,
            etat=etat,
            ville=ville,
            quartier=quartier,
            telephone=user.telephone,
            statut='active',
            nb_vues=random.randint(5, 200),
            date_creation=datetime.utcnow() - timedelta(days=random.randint(0, 30))
        )
        db.session.add(annonce)

    db.session.commit()
    print(f"✅ {len(annonces)} annonces ajoutées au marché")

def creer_prestataires(users):
    """Ajouter des prestataires de services"""
    if Prestataire.query.count() > 2:
        print("⏭️  Prestataires déjà présents")
        return

    prestataires_data = [
        ('Plombier', 'Installation, réparation, dépannage urgent 24h/24',
         'Installation sanitaire, débouchage, fuites', 8, 5000, 50000),
        ('Électricien', 'Installation électrique, dépannage, mise aux normes',
         'Installation, dépannage, panneaux solaires', 10, 7500, 75000),
        ('Mécanicien', 'Toutes marques, diagnostic électronique',
         'Vidange, freinage, moteur, embrayage', 15, 10000, 200000),
        ('Maçon', 'Construction, rénovation, carrelage',
         'Construction, dallage, enduits', 12, 15000, 500000),
        ('Menuisier', 'Meubles sur mesure, portes, fenêtres',
         'Meubles, charpente, portes', 7, 20000, 300000),
        ('Couturier', 'Boubous, complets, retouches',
         'Traditionnels, modernes, uniformes', 6, 3000, 50000),
        ('Informaticien', 'Réparation PC, installation logiciels, dépannage',
         'Réparation, installation, réseaux, formations', 5, 5000, 100000),
        ('Peintre', 'Peinture intérieur et extérieur, décoration',
         'Peinture, décoration, faux plafond', 9, 25000, 400000),
        ('Soudeur', 'Soudure métallique, portails, grilles',
         'Portails, grilles, structures métalliques', 11, 30000, 500000),
        ('Climatisation', 'Installation, entretien, réparation clim',
         'Split, gainable, réparation, recharge gaz', 8, 15000, 150000),
    ]

    users_artisans = [u for u in users if u.type_compte == 'artisan']
    if not users_artisans:
        users_artisans = users[:5]

    for i, (service, desc, spec, exp, tarif_min, tarif_max) in enumerate(prestataires_data):
        user = users_artisans[i % len(users_artisans)]
        prestataire = Prestataire(
            user_id=user.id,
            service_type=service,
            specialites=spec,
            description=desc,
            experience_years=exp,
            tarif_min=tarif_min,
            tarif_max=tarif_max,
            disponible=True,
            ville=user.ville,
            quartier='Centre',
            telephone=user.telephone,
            note_moyenne=round(random.uniform(3.8, 5.0), 1),
            nb_missions=random.randint(5, 150),
            est_verifie=random.choice([True, True, False])
        )
        db.session.add(prestataire)

    db.session.commit()
    print(f"✅ {len(prestataires_data)} prestataires ajoutés")

def creer_offres_emploi(users):
    """Ajouter des offres d'emploi"""
    if OffreEmploi.query.count() > 2:
        print("⏭️  Offres d'emploi déjà présentes")
        return

    offres = [
        ('Développeur Web Full Stack',
         'Nous recherchons un développeur maîtrisant Python/Flask et JavaScript. Expérience 2+ ans requise.',
         'CDI', 'Informatique', 'Niamey', 350000, 600000,
         '2-3 ans', 'Bac+3 en informatique', 'Python, Flask, JavaScript, HTML/CSS'),
        ('Comptable expérimenté',
         'Cabinet comptable recherche comptable pour tenue de comptabilité PME.',
         'CDI', 'Finance', 'Niamey', 250000, 400000,
         '5 ans minimum', 'Bac+3 Comptabilité', 'SAGE, Excel avancé'),
        ('Chef de projet BTP',
         'Grande entreprise BTP recherche chef de projet pour chantiers à Niamey et régions.',
         'CDI', 'BTP', 'Niamey', 500000, 800000,
         '7-10 ans', 'Bac+5 Génie civil', 'Gestion projet, AutoCAD, MS Project'),
        ('Enseignant Mathématiques - Lycée',
         'Lycée privé recherche enseignant qualifié en mathématiques niveau seconde à terminale.',
         'CDD', 'Éducation', 'Niamey', 180000, 250000,
         '3 ans', 'Bac+4 Mathématiques', 'Pédagogie, patience'),
        ('Infirmier(ère) diplômé(e) d\'État',
         'Clinique privée recrute infirmier(ère) pour service urgences.',
         'CDI', 'Santé', 'Niamey', 200000, 300000,
         '2 ans minimum', 'Diplôme IDE', 'Urgences, gardes possibles'),
        ('Commercial terrain',
         'Recherche commercial dynamique pour développer clientèle secteur télécoms.',
         'CDI', 'Commerce', 'Niamey', 150000, 400000,
         '1-2 ans', 'Bac+2', 'Négociation, autonomie, permis B'),
        ('Chauffeur poids lourd',
         'Société de transport recherche chauffeur pour longs trajets Niger-Bénin.',
         'CDD', 'Transport', 'Niamey', 175000, 250000,
         '5 ans', 'Permis EC + FIMO', 'Permis EC, expérience longs trajets'),
        ('Stage - Assistant marketing digital',
         'Startup recherche stagiaire pour community management et création de contenu.',
         'Stage', 'Commerce', 'Niamey', 50000, 75000,
         'Débutant accepté', 'Bac+2 Marketing', 'Réseaux sociaux, créativité'),
        ('Agronome',
         'ONG agricole recherche agronome pour projets de développement rural.',
         'CDD', 'Agriculture', 'Maradi', 300000, 500000,
         '3 ans', 'Bac+5 Agronomie', 'Agriculture durable, formation paysans'),
        ('Chef cuisinier',
         'Restaurant haut de gamme recherche chef cuisinier créatif.',
         'CDI', 'Commerce', 'Niamey', 200000, 350000,
         '5 ans', 'CAP Cuisine', 'Cuisine internationale, gestion équipe'),
    ]

    users_entreprises = [u for u in users if u.type_compte == 'entreprise']
    if not users_entreprises:
        users_entreprises = users[:3]

    for offre in offres:
        titre, desc, contrat, secteur, ville, sal_min, sal_max, exp, formation, comp = offre
        user = random.choice(users_entreprises)

        offre_obj = OffreEmploi(
            recruteur_id=user.id,
            titre=titre,
            entreprise=f"Entreprise {user.nom}",
            description=desc,
            type_contrat=contrat,
            secteur=secteur,
            ville=ville,
            salaire_min=sal_min,
            salaire_max=sal_max,
            experience=exp,
            formation=formation,
            competences=comp,
            telephone=user.telephone,
            email_contact=f"rh@{user.nom.lower()}.ne",
            est_actif=True,
            nb_vues=random.randint(10, 500),
            date_limite=datetime.utcnow() + timedelta(days=random.randint(15, 90))
        )
        db.session.add(offre_obj)

    db.session.commit()
    print(f"✅ {len(offres)} offres d'emploi ajoutées")

def creer_annonces_agricoles(users):
    """Ajouter des annonces agricoles"""
    if AnnonceAgricole.query.count() > 2:
        print("⏭️  Annonces agricoles déjà présentes")
        return

    annonces_agri = [
        ('vente', 'Mil de qualité', 500, 'kg', 22000, 'Maradi',
         'Mil bien conservé, récolte 2024, prix négociable pour grandes quantités'),
        ('vente', 'Niébé (haricot)', 200, 'kg', 45000, 'Tahoua',
         'Niébé de qualité supérieure, trié et propre'),
        ('vente', 'Oignon rouge', 1000, 'kg', 175, 'Agadez',
         'Oignon violet de Galmi, réputé mondialement'),
        ('achat', 'Recherche arachide', 2000, 'kg', 350, 'Niamey',
         'Cherche arachide décortiquée pour transformation en huile'),
        ('vente', 'Bétail - 5 bovins', 5, 'tête', 450000, 'Zinder',
         'Zébus en bonne santé, âge 3-5 ans'),
        ('vente', 'Sorgho blanc', 800, 'kg', 18000, 'Dosso',
         'Sorgho de qualité, séché et bien conservé'),
        ('location', 'Tracteur agricole', 1, 'jour', 45000, 'Niamey',
         'Location tracteur avec chauffeur, tarif journalier'),
        ('vente', 'Semences de mil améliorées', 50, 'kg', 800, 'Maradi',
         'Semences certifiées INRAN, haut rendement'),
    ]

    for type_ann, produit, qte, unite, prix, ville, desc in annonces_agri:
        user = random.choice(users)
        annonce = AnnonceAgricole(
            user_id=user.id,
            type_annonce=type_ann,
            produit=produit,
            quantite=qte,
            unite=unite,
            prix=prix,
            description=desc,
            ville=ville,
            telephone=user.telephone,
            est_actif=True,
            date_creation=datetime.utcnow() - timedelta(days=random.randint(0, 20))
        )
        db.session.add(annonce)

    db.session.commit()
    print(f"✅ {len(annonces_agri)} annonces agricoles ajoutées")

def creer_actualites_supplementaires():
    """Ajouter plus d'actualités"""
    if Actualite.query.count() > 5:
        print("⏭️  Actualités déjà présentes")
        return

    admin = User.query.filter_by(type_compte='admin').first()
    admin_id = admin.id if admin else 1

    actus = [
        ('Nouvelle route Niamey-Dosso : travaux terminés',
         'Les travaux de réhabilitation de la route Niamey-Dosso sont terminés. La circulation est de nouveau fluide sur cet axe majeur du Niger.',
         'Routes', 'Niamey', False),
        ('Alerte météo : Fortes pluies attendues',
         'La Direction de la Météorologie annonce de fortes pluies sur les régions de Niamey, Tillabéri et Dosso ce week-end. Prudence sur les routes.',
         'Alerte météo', 'Niamey', True),
        ('Campagne de vaccination gratuite contre la méningite',
         'Le Ministère de la Santé lance une campagne nationale de vaccination gratuite du 15 au 30 du mois. Rendez-vous dans les centres de santé.',
         'Santé', 'Niamey', False),
        ('Coupure d\'électricité programmée - Quartier Yantala',
         'La NIGELEC informe d\'une coupure d\'électricité prévue mardi de 9h à 15h dans le quartier Yantala pour des travaux de maintenance.',
         'Électricité', 'Niamey', True),
        ('Ouverture du nouveau marché de Katako',
         'Le nouveau marché de Katako a ouvert ses portes. Plus de 500 commerçants y sont installés avec des infrastructures modernes.',
         'Info officielle', 'Niamey', False),
        ('Bourses d\'études pour étudiants nigériens',
         'Le gouvernement annonce l\'ouverture des candidatures pour les bourses d\'études à l\'étranger. Date limite : fin du mois.',
         'Info officielle', 'Niamey', False),
    ]

    for titre, contenu, cat, ville, urgent in actus:
        actu = Actualite(
            titre=titre,
            contenu=contenu,
            categorie=cat,
            ville=ville,
            est_urgent=urgent,
            auteur_id=admin_id,
            est_publie=True,
            nb_vues=random.randint(20, 800),
            date_creation=datetime.utcnow() - timedelta(days=random.randint(0, 15))
        )
        db.session.add(actu)

    db.session.commit()
    print(f"✅ {len(actus)} actualités ajoutées")

def creer_prix_marches_supplementaires():
    """Ajouter plus de prix de marchés"""
    if PrixMarche.query.count() > 10:
        print("⏭️  Prix marchés déjà présents")
        return

    prix_data = [
        ('Maïs', 'céréales', 220, 260, 'kg', 'Katako', 'Niamey'),
        ('Fonio', 'céréales', 500, 600, 'kg', 'Grand Marché', 'Niamey'),
        ('Arachide décortiquée', 'légumineuses', 900, 1100, 'kg', 'Grand Marché', 'Niamey'),
        ('Sésame', 'légumineuses', 800, 1000, 'kg', 'Marché central', 'Maradi'),
        ('Pomme de terre', 'légumes', 400, 500, 'kg', 'Katako', 'Niamey'),
        ('Chou', 'légumes', 300, 400, 'kg', 'Katako', 'Niamey'),
        ('Carotte', 'légumes', 500, 700, 'kg', 'Katako', 'Niamey'),
        ('Poivron', 'légumes', 600, 800, 'kg', 'Katako', 'Niamey'),
        ('Mangue', 'fruits', 300, 500, 'kg', 'Grand Marché', 'Niamey'),
        ('Orange', 'fruits', 400, 600, 'kg', 'Grand Marché', 'Niamey'),
        ('Banane', 'fruits', 500, 700, 'kg', 'Grand Marché', 'Niamey'),
        ('Datte', 'fruits', 2000, 3500, 'kg', 'Marché', 'Agadez'),
        ('Mouton', 'bétail', 45000, 85000, 'tête', 'Marché à bétail', 'Niamey'),
        ('Chèvre', 'bétail', 25000, 45000, 'tête', 'Marché à bétail', 'Maradi'),
        ('Poule', 'volaille', 3500, 5000, 'tête', 'Grand Marché', 'Niamey'),
        ('Œufs', 'volaille', 2500, 3000, 'plateau (30)', 'Grand Marché', 'Niamey'),
        ('Engrais NPK', 'intrants', 22000, 25000, 'sac 50kg', 'Central Agri', 'Niamey'),
        ('Urée', 'intrants', 18000, 21000, 'sac 50kg', 'Central Agri', 'Niamey'),
    ]

    for produit, cat, prix_min, prix_max, unite, marche, ville in prix_data:
        prix = PrixMarche(
            produit=produit,
            categorie=cat,
            prix_min=prix_min,
            prix_max=prix_max,
            unite=unite,
            marche=marche,
            ville=ville,
            date_releve=datetime.utcnow() - timedelta(days=random.randint(0, 5))
        )
        db.session.add(prix)

    db.session.commit()
    print(f"✅ {len(prix_data)} prix de marchés ajoutés")

def creer_etablissements_sante_supplementaires():
    """Ajouter plus d'établissements de santé"""
    if EtablissementSante.query.count() > 3:
        print("⏭️  Établissements santé déjà présents")
        return

    etabs = [
        ('Hôpital Général de Référence', 'hôpital',
         'Route Nationale 1', 'Niamey', 'Lamordé',
         '+227 20 31 51 10', '24h/24', True),
        ('CHU de Lamordé', 'hôpital',
         'Route de Torodi', 'Niamey', 'Lamordé',
         '+227 20 31 55 33', '24h/24', True),
        ('Clinique Gamkallé', 'clinique',
         'Avenue François Mitterrand', 'Niamey', 'Gamkallé',
         '+227 20 74 12 34', '24h/24', True),
        ('Clinique Pasteur', 'clinique',
         'Rue de la Corniche', 'Niamey', 'Plateau',
         '+227 20 73 45 67', '7h-22h', False),
        ('Cabinet Dr. Amadou', 'cabinet',
         'Quartier Terminus', 'Niamey', 'Terminus',
         '+227 96 12 34 56', 'Lun-Ven 8h-17h', False),
        ('Pharmacie de Nuit', 'pharmacie',
         'Rond-point Kennedy', 'Niamey', 'Yantala',
         '+227 20 74 55 66', '20h-8h', False),
        ('Pharmacie Rive Droite', 'pharmacie',
         'Route de Tillabéri', 'Niamey', 'Route Tillabéri',
         '+227 20 75 22 44', '7h-22h', False),
        ('Hôpital Régional de Maradi', 'hôpital',
         'Centre-ville', 'Maradi', 'Centre',
         '+227 20 41 03 05', '24h/24', True),
        ('Hôpital Régional de Zinder', 'hôpital',
         'Avenue de la République', 'Zinder', 'Centre',
         '+227 20 51 03 45', '24h/24', True),
    ]

    for nom, type_e, adresse, ville, quartier, tel, horaires, urg in etabs:
        etab = EtablissementSante(
            nom=nom,
            type_etab=type_e,
            adresse=adresse,
            ville=ville,
            quartier=quartier,
            telephone=tel,
            horaires=horaires,
            urgences=urg,
            est_actif=True
        )
        db.session.add(etab)

    db.session.commit()
    print(f"✅ {len(etabs)} établissements de santé ajoutés")

def creer_demarches_supplementaires():
    """Ajouter plus de démarches administratives"""
    if DemarcheAdmin.query.count() > 3:
        print("⏭️  Démarches déjà présentes")
        return

    demarches = [
        ('Obtention d\'un passeport',
         'Procédure pour obtenir un passeport nigérien biométrique.',
         'Direction de la Documentation',
         'CNI, Extrait de naissance, 4 photos, Attestation de résidence',
         '1. Retirer le formulaire\n2. Remplir et joindre les pièces\n3. Payer les frais (30 000 FCFA)\n4. Prise d\'empreintes\n5. Retrait après 15 jours',
         '15 jours', '30 000 FCFA',
         'Direction de la Documentation, Niamey'),

        ('Carte Nationale d\'Identité (CNI)',
         'Demande de nouvelle CNI ou renouvellement.',
         'Commissariat / Mairie',
         'Extrait de naissance, 2 photos, Certificat de nationalité',
         '1. Aller au commissariat\n2. Remplir le formulaire\n3. Prise d\'empreintes et photo\n4. Payer les frais\n5. Retrait sous 2 semaines',
         '15 jours', '5 000 FCFA',
         'Commissariat central de Niamey'),

        ('Permis de conduire',
         'Obtention du permis de conduire (catégorie B, C, D...).',
         'Direction des Transports Terrestres',
         'CNI, Certificat médical, 4 photos, Attestation auto-école',
         '1. Inscription auto-école\n2. Formation code et conduite\n3. Examen théorique\n4. Examen pratique\n5. Retrait du permis',
         '2-3 mois', '75 000 FCFA (auto-école incluse)',
         'DTT, Route de Niamey Nyala'),

        ('Certificat de nationalité',
         'Attestation officielle de nationalité nigérienne.',
         'Tribunal',
         'Extrait de naissance, CNI des parents, Certificat de résidence',
         '1. Requête au tribunal\n2. Enquête administrative\n3. Audience\n4. Délivrance du certificat',
         '1 mois', '10 000 FCFA',
         'Tribunal de grande instance, Niamey'),

        ('Casier judiciaire',
         'Obtention d\'un extrait de casier judiciaire.',
         'Ministère de la Justice',
         'CNI, Extrait de naissance, Timbre fiscal',
         '1. Demande au greffe\n2. Payer les frais\n3. Retrait après 3-7 jours',
         '3-7 jours', '2 500 FCFA',
         'Palais de justice, Niamey'),
    ]

    for titre, desc, min_, doc, etapes, duree, cout, adresse in demarches:
        demarche = DemarcheAdmin(
            titre=titre,
            description=desc,
            ministere=min_,
            documents=doc,
            etapes=etapes,
            duree=duree,
            cout=cout,
            adresse=adresse
        )
        db.session.add(demarche)

    db.session.commit()
    print(f"✅ {len(demarches)} démarches administratives ajoutées")

def main():
    with app.app_context():
        print("\n" + "="*50)
        print("🌱 PEUPLEMENT DE LA BASE DE DONNÉES")
        print("="*50 + "\n")

        users = creer_utilisateurs_demo()
        creer_entreprises_annuaire(users)
        creer_annonces_marketplace(users)
        creer_prestataires(users)
        creer_offres_emploi(users)
        creer_annonces_agricoles(users)
        creer_actualites_supplementaires()
        creer_prix_marches_supplementaires()
        creer_etablissements_sante_supplementaires()
        creer_demarches_supplementaires()

        print("\n" + "="*50)
        print("🎉 BASE DE DONNÉES ENRICHIE AVEC SUCCÈS !")
        print("="*50)
        print("\n📊 Contenu ajouté :")
        print(f"   • {User.query.count()} utilisateurs")
        print(f"   • {EntrepriseAnnuaire.query.count()} entreprises")
        print(f"   • {Annonce.query.count()} annonces")
        print(f"   • {Prestataire.query.count()} prestataires")
        print(f"   • {OffreEmploi.query.count()} offres d'emploi")
        print(f"   • {AnnonceAgricole.query.count()} annonces agricoles")
        print(f"   • {Actualite.query.count()} actualités")
        print(f"   • {PrixMarche.query.count()} prix marchés")
        print(f"   • {EtablissementSante.query.count()} établissements santé")
        print(f"   • {DemarcheAdmin.query.count()} démarches admin")
        print("\n🚀 Rafraîchissez votre navigateur pour voir le contenu !")
        print("\n💡 Comptes de test créés :")
        print("   Téléphone : 90111111 à 91111111")
        print("   Mot de passe : Password123!\n")

if __name__ == '__main__':
    main()