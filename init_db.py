from app import app, db
from models.user import User
from models.annuaire import EntrepriseAnnuaire
from models.health import EtablissementSante
from models.agriculture import PrixMarche
from models.news import Actualite
from models.admin_service import DemarcheAdmin
from datetime import datetime

def init_database():
    with app.app_context():
        db.create_all()
        print("✅ Tables créées avec succès")
        
        # Vérifier si un admin existe
        admin = User.query.filter_by(telephone='00000000').first()
        if not admin:
            admin = User(
                nom='Admin',
                prenom='NigerConnect',
                telephone='00000000',
                email='admin@nigerconnect.ne',
                type_compte='admin',
                ville='Niamey',
                is_verified=True
            )
            admin.set_password('Admin2024!')
            db.session.add(admin)
            db.session.commit()
            print("✅ Compte admin créé : 00000000 / Admin2024!")

        # Données de démonstration - Établissements santé
        if EtablissementSante.query.count() == 0:
            etablissements = [
                EtablissementSante(
                    nom="Hôpital National de Niamey",
                    type_etab="hôpital",
                    adresse="Plateau, Niamey",
                    ville="Niamey",
                    quartier="Plateau",
                    telephone="+227 20 72 25 20",
                    horaires="24h/24",
                    urgences=True
                ),
                EtablissementSante(
                    nom="Pharmacie de l'Amitié",
                    type_etab="pharmacie",
                    adresse="Grand Marché, Niamey",
                    ville="Niamey",
                    quartier="Grand Marché",
                    telephone="+227 20 73 10 15",
                    horaires="8h-22h",
                    urgences=False
                ),
            ]
            db.session.bulk_save_objects(etablissements)
            db.session.commit()
            print("✅ Établissements de santé ajoutés")

        # Données de démonstration - Prix marché
        if PrixMarche.query.count() == 0:
            prix = [
                PrixMarche(produit="Mil", categorie="céréales",
                           prix_min=200, prix_max=250,
                           unite="kg", marche="Grand Marché", ville="Niamey"),
                PrixMarche(produit="Sorgho", categorie="céréales",
                           prix_min=180, prix_max=220,
                           unite="kg", marche="Grand Marché", ville="Niamey"),
                PrixMarche(produit="Riz local", categorie="céréales",
                           prix_min=400, prix_max=450,
                           unite="kg", marche="Grand Marché", ville="Niamey"),
                PrixMarche(produit="Niébé", categorie="légumineuses",
                           prix_min=350, prix_max=400,
                           unite="kg", marche="Grand Marché", ville="Niamey"),
                PrixMarche(produit="Oignon", categorie="légumes",
                           prix_min=150, prix_max=200,
                           unite="kg", marche="Katako", ville="Niamey"),
                PrixMarche(produit="Tomate", categorie="légumes",
                           prix_min=200, prix_max=300,
                           unite="kg", marche="Katako", ville="Niamey"),
            ]
            db.session.bulk_save_objects(prix)
            db.session.commit()
            print("✅ Prix du marché ajoutés")

        # Données demo - Actualités
        if Actualite.query.count() == 0:
            news = [
                Actualite(
                    titre="Bienvenue sur NigerConnect",
                    contenu="NigerConnect est votre super application pour accéder "
                            "à tous les services du Niger depuis votre téléphone.",
                    categorie="Info officielle",
                    ville="Niamey",
                    est_publie=True
                ),
                Actualite(
                    titre="Alerte : Coupure d'eau dans le quartier Plateau",
                    contenu="La SEEN informe les habitants du Plateau d'une coupure "
                            "d'eau prévue ce jeudi de 8h à 16h pour des travaux.",
                    categorie="Eau",
                    ville="Niamey",
                    est_urgent=True,
                    est_publie=True
                ),
            ]
            db.session.bulk_save_objects(news)
            db.session.commit()
            print("✅ Actualités ajoutées")

        # Données demo - Démarches administratives
        if DemarcheAdmin.query.count() == 0:
            demarches = [
                DemarcheAdmin(
                    titre="Obtention d'un extrait de naissance",
                    description="Démarche pour obtenir un extrait d'acte de naissance.",
                    ministere="Mairie",
                    documents="CNI ou passeport des parents, Carnet de vaccination",
                    etapes="1. Se rendre à la mairie\n2. Remplir le formulaire\n3. Payer les frais\n4. Récupérer le document",
                    duree="1 à 3 jours",
                    cout="500 FCFA",
                    adresse="Mairie de Niamey, Plateau"
                ),
                DemarcheAdmin(
                    titre="Création d'une entreprise",
                    description="Procédure de création d'une entreprise au Niger.",
                    ministere="RCCM / Chambre de Commerce",
                    documents="CNI, Photo d'identité, Casier judiciaire, Capital social",
                    etapes="1. Rédiger les statuts\n2. Déposer au RCCM\n3. Publication au Journal Officiel\n4. Ouverture compte bancaire",
                    duree="3 à 7 jours",
                    cout="À partir de 50 000 FCFA",
                    adresse="RCCM, Avenue de l'Indépendance, Niamey"
                ),
            ]
            db.session.bulk_save_objects(demarches)
            db.session.commit()
            print("✅ Démarches administratives ajoutées")
        
        print("\n🎉 Base de données initialisée avec succès !")
        print("📱 Lancez l'application avec : python app.py")

if __name__ == '__main__':
    init_database()