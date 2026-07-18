# routes/payments.py
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import db
from models.payment import Payment, BillPayment
from datetime import datetime

payments_bp = Blueprint('payments', __name__, url_prefix='/payments')


@payments_bp.route('/')
@login_required
def index():
    recent_payments = Payment.query.filter(
        db.or_(Payment.payer_id == current_user.id, Payment.receiver_id == current_user.id)
    ).order_by(Payment.created_at.desc()).limit(10).all()
    
    return render_template('payments/index.html', payments=recent_payments)


@payments_bp.route('/send', methods=['GET', 'POST'])
@login_required
def send():
    if request.method == 'POST':
        amount = float(request.form.get('amount', 0))
        payment_method = request.form.get('payment_method')
        description = request.form.get('description', '')
        receiver_phone = request.form.get('receiver_phone', '')
        
        # Trouver le destinataire
        from models.user import User
        receiver = User.query.filter_by(phone=receiver_phone).first()
        
        payment = Payment(
            payer_id=current_user.id,
            receiver_id=receiver.id if receiver else None,
            payment_type='transfer',
            payment_method=payment_method,
            amount=amount,
            fees=amount * 0.01,  # 1% de frais
            total=amount * 1.01,
            description=description,
            status='completed'  # Simulation
        )
        payment.completed_at = datetime.utcnow()
        
        db.session.add(payment)
        db.session.commit()
        
        flash(f'Paiement de {amount:,.0f} FCFA effectué avec succès !', 'success')
        return redirect(url_for('payments.index'))
    
    return render_template('payments/send.html')


@payments_bp.route('/bills', methods=['GET', 'POST'])
@login_required
def pay_bill():
    if request.method == 'POST':
        bill = BillPayment(
            user_id=current_user.id,
            bill_type=request.form.get('bill_type'),
            provider=request.form.get('provider'),
            account_number=request.form.get('account_number'),
            amount=float(request.form.get('amount', 0)),
            status='completed'  # Simulation
        )
        
        db.session.add(bill)
        db.session.commit()
        
        flash(f'Facture de {bill.amount:,.0f} FCFA payée avec succès !', 'success')
        return redirect(url_for('payments.index'))
    
    return render_template('payments/bills.html')


@payments_bp.route('/history')
@login_required
def history():
    page = request.args.get('page', 1, type=int)
    payments = Payment.query.filter(
        db.or_(Payment.payer_id == current_user.id, Payment.receiver_id == current_user.id)
    ).order_by(Payment.created_at.desc()).paginate(page=page, per_page=20)
    
    return render_template('payments/history.html', payments=payments)