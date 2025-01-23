from flask import render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from app import app, db
from models import NotaryRequest
from SignDocument import NotaryRequestForm
from flask_login import (
    UserMixin, login_user, login_required, logout_user,
    current_user, LoginManager, AnonymousUserMixin
)
from passlib.hash import sha256_crypt
import os
from Register import RegisterForm, LoginForm

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message = "Please log in to access this page."

# Simulated User Database with roles
users = {
    "1": {"id": "1", "username": "admin1", "email": "admin1@example.com", "password": sha256_crypt.hash("adminpass123"), "role": "admin"},
    "2": {"id": "2", "username": "user1", "email": "user1@example.com", "password": sha256_crypt.hash("userpass123"), "role": "user"},
}

# User class with role handling
class User(UserMixin):
    def __init__(self, id, username, email, role):
        self.id = id
        self.username = username
        self.email = email
        self.role = role

    @property
    def is_admin(self):
        return self.role == "admin"  # Admin role check


# User loader function
@login_manager.user_loader
def load_user(user_id):
    user_data = users.get(user_id)
    if user_data:
        return User(user_id, user_data["username"], user_data["email"], user_data["role"])
    return None


# Custom Anonymous User
class Anonymous(AnonymousUserMixin):
    def __init__(self):
        self.username = "Guest"
        self.is_admin = False

login_manager.anonymous_user = Anonymous


# Routes
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/services')
def services():
    return render_template('services.html')


@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.is_admin:
        # Admin sees all requests
        notary_requests = NotaryRequest.query.all()
    else:
        # Non-admin sees only their own requests
        notary_requests = NotaryRequest.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', notary_requests=notary_requests, name=current_user.username)


@app.route('/SignDocument', methods=['GET', 'POST'])
@login_required
def SignDocument():
    form = NotaryRequestForm()
    if request.method == 'POST' and form.validate_on_submit():
        try:
            # Collect form data
            full_name = form.fullName.data
            email = form.email.data
            age = form.age.data
            service_type = form.service_type.data
            comment = form.comment.data
            user_category = form.user_category.data

            # File upload handling
            document_path = None
            uploaded_file = form.document.data
            if uploaded_file:
                filename = secure_filename(uploaded_file.filename)
                document_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                uploaded_file.save(document_path)

            # Save to database
            new_request = NotaryRequest(
                full_name=full_name,
                email=email,
                age=age,
                service_type=service_type,
                comment=comment,
                user_category=user_category,
                document_path=document_path,
                user_id=current_user.id
            )
            db.session.add(new_request)
            db.session.commit()

            flash('Form submitted successfully!', 'success')
            return redirect(url_for('dashboard'))
        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'danger')
    return render_template('SignDocument.html', form=form)


@app.route('/Register', methods=['POST', 'GET'])
def Register():
    form = RegisterForm()
    if form.validate_on_submit():
        flash("User registration not yet implemented.", "info")
        return redirect(url_for('login'))
    return render_template('Register.html', title="Register", form=form)


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = next((user for user in users.values() if user["email"] == form.email.data), None)
        if user and sha256_crypt.verify(form.password.data, user['password']):
            login_user(User(user['id'], user['username'], user['email'], user['role']))
            return redirect(url_for('dashboard'))
        flash("Invalid email or password", "danger")
    return render_template('login.html', title="Login", form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out successfully.", "success")
    return redirect(url_for('login'))
