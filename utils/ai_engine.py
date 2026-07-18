from models.annuaire import EntrepriseAnnuaire
from models.health import EtablissementSante
from models.agriculture import PrixMarche
from models.service import Prestataire
from models.job import OffreEmploi
from models.admin_service import DemarcheAdmin

class NigerConnectAI:
    """Assistant IA local pour NigerConnect"""
    
    def __init__(self):
        self.knowledge_base = {
            'pharmacie': self._chercher_pharmacie,
            'hôpital': self._chercher_hopital,
            'garage': self._chercher_garage,
            'prix': self._chercher_prix,
            'plombier': self._chercher_prestataire,
            'électricien': self._chercher_prestataire,
            'mécanicien': self._chercher_prestataire,
            'emploi': self._chercher_emploi,
            'entreprise': self._infos_creation_entreprise,
        }

    def repondre(self, question: str) -> str:
        question_lower = question.lower()
        
        for mot_cle, fonction in self.knowledge_base.items():
            if mot_cle in question_lower:
                return fonction(question_lower)
        
        return self._reponse_generale(question)

    def _chercher_pharmacie(self, question: str) -> str:
        pharmacies = EtablissementSante.query.filter_by(
            type_etab='pharmacie', est_actif=True
        ).limit(3).all()
        
        if not pharmacies:
            return ("Je n'ai pas trouvé de pharmacie dans ma base de données. "
                    "Consultez la section Santé pour plus d'informations.")
        
        reponse = "🏥 **Pharmacies disponibles :**\n\n"
        for p in pharmacies:
            reponse += f"• **{p.nom}**\n"
            reponse += f"  📍 {p.quartier}, {p.ville}\n"
            reponse += f"  📞 {p.telephone}\n"
            reponse += f"  ⏰ {p.horaires}\n\n"
        return reponse

    def _chercher_hopital(self, question: str) -> str:
        hopitaux = EtablissementSante.query.filter(
            EtablissementSante.type_etab.in_(['hôpital', 'clinique']),
            EtablissementSante.est_actif == True
        ).limit(3).all()
        
        if not hopitaux:
            return "Aucun hôpital trouvé. Appelez le 15 pour les urgences."
        
        reponse = "🏥 **Hôpitaux et cliniques :**\n\n"
        for h in hopitaux:
            reponse += f"• **{h.nom}**\n"
            reponse += f"  📍 {h.adresse}\n"
            reponse += f"  📞 {h.telephone}\n"
            if h.urgences:
                reponse += "  🚨 *Urgences 24h/24*\n"
            reponse += "\n"
        return reponse

    def _chercher_garage(self, question: str) -> str:
        garages = EntrepriseAnnuaire.query.filter_by(
            categorie='Garage', est_verifie=True
        ).limit(3).all()
        
        prestataires = Prestataire.query.filter_by(
            service_type='Mécanicien', disponible=True
        ).limit(3).all()
        
        reponse = "🔧 **Garages et mécaniciens :**\n\n"
        
        if garages:
            reponse += "**Garages enregistrés :**\n"
            for g in garages:
                reponse += f"• {g.nom} - {g.quartier} - {g.telephone}\n"
            reponse += "\n"
        
        if prestataires:
            reponse += "**Mécaniciens disponibles :**\n"
            for p in prestataires:
                user = p.user
                reponse += f"• {user.nom_complet()} - {p.ville} - {p.telephone}\n"
        
        if not garages and not prestataires:
            reponse = ("Aucun garage trouvé. Consultez la section "
                       "**Services** pour trouver un mécanicien.")
        
        return reponse

    def _chercher_prix(self, question: str) -> str:
        # Cherche un produit dans la question
        produits = ['mil', 'sorgho', 'riz', 'niébé', 'oignon', 'tomate',
                    'ciment', 'fer', 'maïs', 'arachide']
        
        produit_trouve = None
        for p in produits:
            if p in question:
                produit_trouve = p
                break
        
        if produit_trouve:
            prix = PrixMarche.query.filter(
                PrixMarche.produit.ilike(f'%{produit_trouve}%')
            ).order_by(PrixMarche.date_releve.desc()).first()
            
            if prix:
                return (f"💰 **Prix du {prix.produit}**\n\n"
                        f"• Marché : {prix.marche}, {prix.ville}\n"
                        f"• Prix : {int(prix.prix_min)} - {int(prix.prix_max)} FCFA/{prix.unite}\n"
                        f"• Dernière mise à jour : {prix.date_releve.strftime('%d/%m/%Y')}")
        
        # Prix généraux
        prix_liste = PrixMarche.query.order_by(
            PrixMarche.date_releve.desc()
        ).limit(5).all()
        
        if not prix_liste:
            return "Aucun prix disponible. Consultez la section Agriculture."
        
        reponse = "📊 **Prix actuels au marché :**\n\n"
        for p in prix_liste:
            reponse += f"• {p.produit} : {int(p.prix_min)}-{int(p.prix_max)} FCFA/{p.unite}\n"
        return reponse

    def _chercher_prestataire(self, question: str) -> str:
        types = {
            'plombier': 'Plombier',
            'électricien': 'Électricien',
            'mécanicien': 'Mécanicien',
            'informaticien': 'Informaticien',
            'maçon': 'Maçon',
        }
        
        service = None
        for mot, type_service in types.items():
            if mot in question:
                service = type_service
                break
        
        if not service:
            return "Précisez le type de prestataire recherché."
        
        prestataires = Prestataire.query.filter_by(
            service_type=service, disponible=True
        ).limit(3).all()
        
        if not prestataires:
            return (f"Aucun {service.lower()} disponible actuellement. "
                    f"Consultez la section **Services à domicile**.")
        
        reponse = f"🔨 **{service}s disponibles :**\n\n"
        for p in prestataires:
            user = p.user
            reponse += f"• **{user.nom_complet()}**\n"
            reponse += f"  📞 {p.telephone or user.telephone}\n"
            reponse += f"  📍 {p.ville}\n"
            if p.tarif_min:
                reponse += f"  💰 À partir de {int(p.tarif_min):,} FCFA\n"
            reponse += "\n"
        return reponse

    def _chercher_emploi(self, question: str) -> str:
        offres = OffreEmploi.query.filter_by(
            est_actif=True
        ).order_by(OffreEmploi.date_creation.desc()).limit(3).all()
        
        if not offres:
            return "Aucune offre d'emploi disponible. Consultez la section **Emploi**."
        
        reponse = "💼 **Offres d'emploi récentes :**\n\n"
        for o in offres:
            reponse += f"• **{o.titre}**\n"
            reponse += f"  🏢 {o.entreprise or 'Non précisé'}\n"
            reponse += f"  📍 {o.ville} | {o.type_contrat}\n"
            if o.salaire_min:
                reponse += f"  💰 {int(o.salaire_min):,} FCFA\n"
            reponse += "\n"
        return reponse

    def _infos_creation_entreprise(self, question: str) -> str:
        demarche = DemarcheAdmin.query.filter(
            DemarcheAdmin.titre.ilike('%entreprise%')
        ).first()
        
        if demarche:
            return (f"🏢 **{demarche.titre}**\n\n"
                    f"**Documents nécessaires :**\n{demarche.documents}\n\n"
                    f"**Étapes :**\n{demarche.etapes}\n\n"
                    f"**Durée :** {demarche.duree}\n"
                    f"**Coût :** {demarche.cout}\n"
                    f"**Adresse :** {demarche.adresse}")
        
        return ("Pour créer une entreprise au Niger :\n\n"
                "1. Rédigez vos statuts\n"
                "2. Déposez au RCCM\n"
                "3. Publiez au Journal Officiel\n"
                "4. Ouvrez un compte bancaire professionnel\n\n"
                "Consultez la section **Administration** pour plus de détails.")

    def _reponse_generale(self, question: str) -> str:
        suggestions = [
            "🔍 Essayez de rechercher dans l'annuaire",
            "🛒 Consultez le marché numérique",
            "🔧 Trouvez un prestataire de services",
            "💼 Parcourez les offres d'emploi",
            "🌾 Consultez les prix agricoles",
        ]
        
        reponse = ("Je n'ai pas trouvé de réponse précise à votre question. "
                   "Voici ce que vous pouvez faire :\n\n")
        for s in suggestions:
            reponse += f"{s}\n"
        
        reponse += ("\n💡 **Posez votre question différemment**, par exemple :\n"
                    "• *Où trouver une pharmacie ?*\n"
                    "• *Quel est le prix du mil ?*\n"
                    "• *Comment créer une entreprise ?*")
        return reponse