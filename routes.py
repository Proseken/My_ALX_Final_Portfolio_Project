from flask import render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from app import app, db
from models import NotaryRequest
from forms import NotaryRequestForm
import os

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/submissions')
def view_submissions():
    # Query all records from the database
    submissions = NotaryRequest.query.order_by(NotaryRequest.date_created.desc()).all()
    return render_template('submissions.html', submissions=submissions)

@app.route('/Register')
def Register():
    return render_template('Register.html')

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
                document_path=document_path
            )
            db.session.add(new_request)
            db.session.commit()

            flash('Form submitted successfully!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'danger')
            return redirect(url_for('SignDocument'))

    return render_template('SignDocument.html', form=form)
