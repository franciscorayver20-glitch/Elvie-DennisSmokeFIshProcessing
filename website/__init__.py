from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager    
from flask_migrate import Migrate
from flask_mail import Mail
import os

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'asdasdasd asdasdasd'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}' 
    db.init_app(app)
    migrate = Migrate(app, db)

    # ---------- Email configuration (add this block) ----------
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'          # or your SMTP server
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')   # set environment variable
    app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')   # set environment variable
    app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER')
    mail = Mail(app)
    # Store mail instance for access in auth blueprint (using current_app)
    app.extensions['mail'] = mail
    # ---------------------------------------------------------

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    
    from .models import User, Product, Transaction, Personnel

    create_database(app)
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    from .models import User, Product, Transaction, Personnel, Sheet, ProductSheet, SheetProduct, TransactionItem, ProductSnapshot
    from werkzeug.security import generate_password_hash

    with app.app_context():
        db.create_all()

        admin_email = 'admin@tinapa.com'
        if not User.query.filter_by(email=admin_email).first():
            new_admin = User(
                email=admin_email,
                first_name='Admin',
                password=generate_password_hash('admin123', method='pbkdf2:sha256'),
                is_admin=True
            )
            db.session.add(new_admin)
            db.session.commit()
            print('--- Database Ignited & Admin Created ---')
        else:
            print('--- Database already exists, skipping seed ---')