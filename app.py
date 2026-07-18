from flask import Flask, render_template, redirect, url_for
from flask_login import current_user
from config import config
from models import db, login_manager, bcrypt
import os

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Initialisation extensions
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    login_manager.login_view        = 'auth.connexion'
    login_manager.login_message     = 'Veuillez vous connecter.'
    login_manager.login_message_category = 'warning'

    # User loader
    from models.user import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Enregistrement des blueprints
    from routes.auth           import auth_bp
    from routes.dashboard      import dashboard_bp
    from routes.annuaire       import annuaire_bp
    from routes.marketplace    import marketplace_bp
    from routes.services       import services_bp
    from routes.transport      import transport_bp
    from routes.payments       import payments_bp
    from routes.health         import health_bp
    from routes.jobs           import jobs_bp
    from routes.agriculture    import agriculture_bp
    from routes.admin_services import admin_services_bp
    from routes.news           import news_bp
    from routes.ai_assistant   import ai_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(annuaire_bp)
    app.register_blueprint(marketplace_bp)
    app.register_blueprint(services_bp)
    app.register_blueprint(transport_bp)
    app.register_blueprint(payments_bp)
    app.register_blueprint(health_bp)
    app.register_blueprint(jobs_bp)
    app.register_blueprint(agriculture_bp)
    app.register_blueprint(admin_services_bp)
    app.register_blueprint(news_bp)
    app.register_blueprint(ai_bp)

    # Route principale
    from flask import Blueprint
    main_bp = Blueprint('main', __name__)

    @main_bp.route('/')
    def index():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard.index'))
        return render_template('index.html')

    app.register_blueprint(main_bp)

    # Filtre Jinja personnalisé
    @app.template_filter('prix_format')
    def prix_format(montant):
        if montant is None:
            return '-'
        return f"{int(montant):,} FCFA".replace(',', ' ')

    @app.template_filter('temps_ecoule')
    def temps_ecoule_filter(date):
        from utils.helpers import temps_ecoule
        return temps_ecoule(date)

    # Gestionnaire d'erreurs
    @app.errorhandler(404)
    def not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def server_error(e):
        return render_template('errors/500.html'), 500

    # Créer dossiers nécessaires
    os.makedirs(os.path.join(app.root_path, 'static', 'uploads'), exist_ok=True)

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)