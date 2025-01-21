from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, TextAreaField, RadioField, FileField, BooleanField
from wtforms.validators import InputRequired, Email, Optional, NumberRange

# Flask-WTF form
class NotaryRequestForm(FlaskForm):
    fullName = StringField('Full Name', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(), Email()])
    age = IntegerField('Age (optional)', validators=[Optional(), NumberRange(min=10, max=99)])
    service_type = SelectField(
        'Service Type',
        choices=[
            ('select', '__select a service__'),
            ('document_notarization', 'Document Notarization'),
            ('affidavit', 'Affidavit Preparation'),
            ('certified_copy', 'Certified True Copy'),
            ('oaths', 'Oaths and Declarations'),
            ('wills', 'Wills and Testaments'),
            ('contract', 'Contract Notarization'),
            ('other', 'Other')
        ],
        validators=[InputRequired()]
    )
    document = FileField('Upload Document', validators=[Optional()])
    terms = BooleanField('I agree to the terms and conditions', validators=[InputRequired()])
    user_category = RadioField(
        'This document is for',
        choices=[
            ('Minor', 'Minor'),
            ('Adult', 'Adult (Parent/Guardian)'),
            ('Acquaintance', 'Relative or Friend')
        ],
        validators=[InputRequired()]
    )
    comment = TextAreaField('Any comments or suggestions?', validators=[Optional()])
