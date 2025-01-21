from flask import render_template, request, redirect, session, url_for, flash
from werkzeug.utils import secure_filename
from app import app, db
from models import NotaryRequest
from SignDocument import NotaryRequestForm
from flask_login import UserMixin, login_user, login_required, logout_user, current_user, LoginManager
from passlib.hash import sha256_crypt
import os
from Register import RegisterForm, LoginForm

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"  # Redirect to 'login' if not authenticated
login_manager.login_message = "Please log in to access this page."

# Simulated User Database with roles (admin and user)
users = {
    "1": {"id": "1", "username": "admin1", "email": "admin1@example.com", "password": sha256_crypt.hash("adminpass123"), "role": "admin"},
    "2": {"id": "2", "username": "admin2", "email": "admin2@example.com", "password": sha256_crypt.hash("adminpass456"), "role": "admin"},
    "3": {"id": "3", "username": "admin3", "email": "admin3@example.com", "password": sha256_crypt.hash("adminpass789"), "role": "admin"},
    "4": {"id": "4", "username": "admin4", "email": "admin4@example.com", "password": sha256_crypt.hash("adminpass101"), "role": "admin"},
    "5": {"id": "5", "username": "user1", "email": "user1@example.com", "password": sha256_crypt.hash("userpass123"), "role": "user"},
    "6": {"id": "6", "username": "user2", "email": "user2@example.com", "password": sha256_crypt.hash("userpass456"), "role": "user"},
    "7": {"id": "7", "username": "user3", "email": "user3@example.com", "password": sha256_crypt.hash("userpass789"), "role": "user"},
    "8": {"id": "8", "username": "user4", "email": "user4@example.com", "password": sha256_crypt.hash("userpass101"), "role": "user"}
}


# User Class with Role Handling
class User(UserMixin):
    def __init__(self, id, username, email, role):
        self.id = id
        self.username = username
        self.email = email
        self.role = role  # Store the role

    def is_admin(self):
        return self.role == "admin"  # Check if the user is an admin

# User Loader Function
@login_manager.user_loader
def load_user(user_id):
    user_data = users.get(user_id)
    if user_data:
        return User(user_id, user_data["username"], user_data["email"], user_data["role"])
    return None

# Routes
@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.is_admin():
        # If the user is an admin, show all notary requests
        notary_requests = NotaryRequest.query.all()
    else:
        # If the user is not an admin, show only their own notary requests
        notary_requests = NotaryRequest.query.filter_by(user_id=current_user.id).all()

    return render_template('dashboard.html', notary_requests=notary_requests, name=current_user.username)

@app.route('/SignDocument', methods=['GET', 'POST'])
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
                user_id=current_user.id  # Link the request to the current user
            )
            db.session.add(new_request)
            db.session.commit()

            flash('Form submitted successfully!', 'success')
            return redirect(url_for('dashboard'))
        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'danger')
            return redirect(url_for('SignDocument'))

    return render_template('SignDocument.html', form=form)


# Registration route
@app.route('/Register', methods=['POST', 'GET'])
def Register():
    form = RegisterForm()
    if form.validate_on_submit():
        # Logic to handle user registration (not implemented)
        return redirect(url_for('login'))
    return render_template('Register.html', title="Register", form=form)

# Login route
@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Check if email exists in users dictionary
        user = next((user for user in users.values() if user["email"] == form.email.data), None)
        if user and sha256_crypt.verify(form.password.data, user['password']):
            # Create User object and log in
            login_user(User(user['id'], user['username'], user['email'], user['role']))
            return redirect(url_for('dashboard'))
        flash("Invalid email or password", "danger")
    return render_template('login.html', title="Login", form=form)


# Logout part
@app.route('/logout')
@login_required
def logout():
    # Log out the user
    logout_user()
    
    # Provide feedback
    flash("You have been logged out successfully.", "success")
    
    # Redirect to login page or home page
    return redirect(url_for('login'))  # Replace 'login' with the desired route