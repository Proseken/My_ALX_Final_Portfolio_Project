from app import db
from datetime import datetime

# Database model
class NotaryRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=True)
    service_type = db.Column(db.String(50), nullable=False)
    comment = db.Column(db.Text, nullable=True)
    user_category = db.Column(db.String(50), nullable=False)
    document_path = db.Column(db.String(200), nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<NotaryRequest {self.id}>'
