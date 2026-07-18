from flask import Blueprint, render_template, request
from models.admin_service import DemarcheAdmin

admin_services_bp = Blueprint('admin_services', __name__,
                               url_prefix='/administration')

@admin_services_bp.route('/')
def index():
    recherche = request.args.get('q', '')
    ministere = request.args.get('ministere', '')

    query = DemarcheAdmin.query

    if recherche:
        query = query.filter(
            DemarcheAdmin.titre.ilike(f'%{recherche}%') |
            DemarcheAdmin.description.ilike(f'%{recherche}%')
        )
    if ministere:
        query = query.filter_by(ministere=ministere)

    demarches  = query.order_by(DemarcheAdmin.titre).all()
    ministeres = db.session.query(
        DemarcheAdmin.ministere
    ).distinct().all() if False else []

    from models import db
    ministeres = [m[0] for m in
                  db.session.query(DemarcheAdmin.ministere).distinct().all()
                  if m[0]]

    return render_template('admin_services/index.html',
                           demarches=demarches,
                           ministeres=ministeres,
                           recherche=recherche,
                           ministere_actif=ministere)

@admin_services_bp.route('/<int:id>')
def detail(id):
    demarche = DemarcheAdmin.query.get_or_404(id)
    return render_template('admin_services/detail.html', demarche=demarche)