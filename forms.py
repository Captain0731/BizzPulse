from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, EmailField, validators
from wtforms.validators import DataRequired, Email, Length, Optional

class ContactForm(FlaskForm):
    """Form for contact submissions"""
    
    name = StringField('Name', 
                      validators=[
                          DataRequired(message="Name is required"),
                          Length(min=2, max=100, message="Name must be between 2 and 100 characters")
                      ])
    
    email = EmailField('Email', 
                      validators=[
                          DataRequired(message="Email is required"),
                          Email(message="Please enter a valid email address"),
                          Length(max=120, message="Email must be less than 120 characters")
                      ])
    
    subject = StringField('Subject', 
                         validators=[
                             Optional(),
                             Length(max=200, message="Subject must be less than 200 characters")
                         ])
    
    message = TextAreaField('Message', 
                           validators=[
                               DataRequired(message="Message is required"),
                               Length(min=10, max=2000, message="Message must be between 10 and 2000 characters")
                           ])
    
    phone = StringField('Phone', 
                       validators=[
                           Optional(),
                           Length(max=20, message="Phone number must be less than 20 characters")
                       ])
    
    company = StringField('Company', 
                         validators=[
                             Optional(),
                             Length(max=100, message="Company name must be less than 100 characters")
                         ])

class NewsletterForm(FlaskForm):
    """Form for newsletter subscriptions"""
    
    email = EmailField('Email', 
                      validators=[
                          DataRequired(message="Email is required"),
                          Email(message="Please enter a valid email address"),
                          Length(max=120, message="Email must be less than 120 characters")
                      ])
