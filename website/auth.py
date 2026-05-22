import email

from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from .models import User
from .import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from datetime import datetime, timedelta
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                user.last_login = datetime.now()
                user.is_online = True
                db.session.commit()
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')
    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    current_user.is_online = False
    db.session.commit()
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match. ', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(
                email=email,
                first_name=first_name,
                password=generate_password_hash(password1),
                date_created=datetime.now()
            )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            new_user.last_login = datetime.now()
            new_user.is_online = True
            db.session.commit()
            flash('Account created !', category='success')
            return redirect(url_for('views.home'))
    return render_template("sign_up.html", user=current_user)


# Helper functions for password reset
def generate_reset_token(email):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt='password-reset-salt')


def verify_reset_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token, salt='password-reset-salt', max_age=expiration)
    except:
        return None
    return email


@auth.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email').strip().lower()
        user = User.query.filter_by(email=email).first()
        if not user:
            flash('No account found with that email address.', 'error')
            return redirect(url_for('auth.forgot_password'))

        token = generate_reset_token(email)
        user.reset_token = token
        user.token_expiry = datetime.now() + timedelta(hours=1)
        db.session.commit()

        reset_link = url_for('auth.reset_password', token=token, _external=True)

        # Retrieve the mail instance stored in app extensions
        mail = current_app.extensions['mail']
        msg = Message('Password Reset Request', recipients=[email])
        msg.body = f'''To reset your password, visit the following link:
{reset_link}

If you did not make this request, simply ignore this email.
'''
        try:
            mail.send(msg)
            flash('A password reset link has been sent to your email address.', 'success')
        except Exception as e:
            flash('Error sending email. Please try again later.', 'error')
            print(f"Email error: {e}")
        return redirect(url_for('auth.login'))

    return render_template('forgot_password.html')


@auth.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    user = User.query.filter_by(reset_token=token).first()
    if not user or user.token_expiry < datetime.now():
        flash('The reset link is invalid or has expired.', 'error')
        return redirect(url_for('auth.forgot_password'))

    if request.method == 'POST':
        password = request.form.get('password')
        confirm = request.form.get('confirm_password')

        if len(password) < 7:
            flash('Password must be at least 7 characters.', 'error')
            return redirect(url_for('auth.reset_password', token=token))
        if password != confirm:
            flash('Passwords do not match.', 'error')
            return redirect(url_for('auth.reset_password', token=token))

        user.password = generate_password_hash(password, method='pbkdf2:sha256')
        user.last_updated = datetime.now()
        user.reset_token = None
        user.token_expiry = None
        db.session.commit()

        flash('Your password has been reset. Please log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('reset_password.html', token=token)