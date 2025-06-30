from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectMultipleField, widgets
from wtforms.validators import DataRequired, Length, ValidationError

class PostForm(FlaskForm):
    """Form for creating and editing blog posts"""
    
    title = StringField('Title', validators=[
        DataRequired(message='Title is required'),
        Length(min=1, max=200, message='Title must be between 1 and 200 characters')
    ])
    
    body = TextAreaField('Content', validators=[
        DataRequired(message='Content is required'),
        Length(min=1, message='Content cannot be empty')
    ])
    
    is_published = BooleanField('Publish now')
    
    tags = SelectMultipleField('Tags', 
                              widget=widgets.ListWidget(prefix_label=False),
                              option_widget=widgets.CheckboxInput())
    
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        # Tags will be populated dynamically in the route
    
    def validate_title(self, field):
        """Custom validation for title"""
        if field.data and len(field.data.strip()) == 0:
            raise ValidationError('Title cannot be only whitespace')
    
    def validate_body(self, field):
        """Custom validation for body"""
        if field.data and len(field.data.strip()) == 0:
            raise ValidationError('Content cannot be only whitespace')
