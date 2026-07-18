import requests
from flask import current_app

class SMSGateway:
    """Gateway SMS pour Orange Niger / Airtel"""
    
    def __init__(self):
        self.api_key = current_app.config.get('SMS_API_KEY', '')
        self.sender  = current_app.config.get('SMS_SENDER', 'NigerConnect')
    
    def envoyer_sms(self, telephone: str, message: str) -> bool:
        """Envoie un SMS"""
        if not self.api_key:
            # Mode développement : afficher dans les logs
            current_app.logger.info(
                f"[SMS DEV] À: {telephone} | Message: {message}"
            )
            return True
        
        try:
            # Adapter selon votre opérateur SMS
            response = requests.post(
                'https://api.sms-niger.ne/send',
                json={
                    'api_key': self.api_key,
                    'from': self.sender,
                    'to': telephone,
                    'message': message
                },
                timeout=10
            )
            return response.status_code == 200
        except Exception as e:
            current_app.logger.error(f"Erreur SMS: {e}")
            return False
    
    def envoyer_code_verification(self, telephone: str, code: str) -> bool:
        message = (f"NigerConnect - Votre code de vérification : {code}\n"
                   f"Valable 10 minutes.")
        return self.envoyer_sms(telephone, message)
    
    def notifier_demande(self, telephone: str, service: str) -> bool:
        message = (f"NigerConnect - Nouvelle demande de service : {service}.\n"
                   f"Connectez-vous pour répondre.")
        return self.envoyer_sms(telephone, message)