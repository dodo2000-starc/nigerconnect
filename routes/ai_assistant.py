from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from utils.ai_engine import NigerConnectAI

ai_bp = Blueprint('ai', __name__, url_prefix='/assistant')

@ai_bp.route('/')
def index():
    questions_exemples = [
        "Où trouver une pharmacie ouverte ?",
        "Quel est le prix du mil aujourd'hui ?",
        "Comment créer une entreprise au Niger ?",
        "Où trouver un plombier à Niamey ?",
        "Quels hôpitaux sont disponibles ?",
        "Y a-t-il des offres d'emploi disponibles ?",
    ]
    return render_template('ai/index.html',
                           questions_exemples=questions_exemples)

@ai_bp.route('/question', methods=['POST'])
def poser_question():
    data     = request.get_json()
    question = data.get('question', '').strip()

    if not question:
        return jsonify({'reponse': 'Veuillez poser une question.'}), 400

    if len(question) > 500:
        return jsonify({'reponse': 'Question trop longue (max 500 caractères).'}), 400

    ai      = NigerConnectAI()
    reponse = ai.repondre(question)

    return jsonify({'reponse': reponse, 'question': question})