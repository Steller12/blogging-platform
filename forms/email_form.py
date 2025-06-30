from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Email, ValidationError
import re

class EmailForm(FlaskForm):
    """Form for testing email validation"""
    
    username = StringField('Username', validators=[
        DataRequired(message='Username is required')
    ])
    
    email = StringField('Email', validators=[
        DataRequired(message='Email is required'),
        Email(message='Invalid email address')
    ])
    
    def validate_email(self, field):
        """Additional email validation"""
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if field.data and not re.match(email_pattern, field.data):
            raise ValidationError('Please enter a valid email address')
