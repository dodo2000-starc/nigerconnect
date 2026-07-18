from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from models import db
from models.payment import Transaction
from utils.helpers import generer_reference

payments_bp = Blueprint('payments', __name__, url_prefix='/paiements')

OPERATEURS = ['Orange Money', 'Airtel Money', 'Moov Money']
TYPES_FACTURE = ['Eau (SEEN)', 'Électricité (NIGELEC)', 'Internet', 'Téléphone']

@payments_bp.route('/')
@login_required
def index():
    transactions = Transaction.query.filter_by(
        user_id=current_user.id
    ).order_by(Transaction.date_creation.desc()).limit(10).all()

    return render_template('payments/index.html',
                           transactions=transactions,
                           operateurs=OPERATEURS,
                           types_facture=TYPES_FACTURE)

@payments_bp.route('/mobile-money', methods=['GET', 'POST'])
@login_required
def mobile_money():
    if request.method == 'POST':
        montant   = float(request.form.get('montant', 0))
        operateur = request.form.get('operateur')
        telephone = request.form.get('telephone')

        if montant <= 0:
            flash('Montant invalide.', 'danger')
            return render_template('payments/mobile_money.html',
                                   operateurs=OPERATEURS)

        ref = generer_reference()
        transaction = Transaction(
            user_id          = current_user.id,
            type_transaction = 'mobile_money',
            montant          = montant,
            reference        = ref,
            operateur        = operateur,
            description      = f'Transfert vers {telephone}',
            statut           = 'en_attente',
        )
        db.session.add(transaction)
        db.session.commit()

        # Ici on intégrerait l'API Orange Money / Airtel
        # Pour la démo, on simule un succès
        transaction.statut = 'succes'
        db.session.commit()

        flash(f'Transfert de {int(montant):,} FCFA initié. Référence : {ref}',
              'success')
        return redirect(url_for('payments.index'))

    return render_template('payments/mobile_money.html',
                           operateurs=OPERATEURS)

@payments_bp.route('/facture', methods=['GET', 'POST'])
@login_required
def payer_facture():
    if request.method == 'POST':
        type_facture  = request.form.get('type_facture')
        numero_compte = request.form.get('numero_compte')
        montant       = float(request.form.get('montant', 0))

        ref = generer_reference()
        transaction = Transaction(
            user_id          = current_user.id,
            type_transaction = 'facture',
            montant          = montant,
            reference        = ref,
            description      = f'{type_facture} - Compte {numero_compte}',
            statut           = 'succes',
        )
        db.session.add(transaction)
        db.session.commit()

        flash(f'Facture {type_facture} payée. Référence : {ref}', 'success')
        return redirect(url_for('payments.index'))

    return render_template('payments/facture.html',
                           types_facture=TYPES_FACTURE)

@payments_bp.route('/historique')
@login_required
def historique():
    page = request.args.get('page', 1, type=int)
    transactions = Transaction.query.filter_by(
        user_id=current_user.id
    ).order_by(
        Transaction.date_creation.desc()
    ).paginate(page=page, per_page=20, error_out=False)

    return render_template('payments/historique.html',
                           transactions=transactions)