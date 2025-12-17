from datetime import datetime
from app import db


class Contact(db.Model):
    """Model for storing contact form submissions"""
    
    __tablename__ = 'contacts'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(200), nullable=True)
    message = db.Column(db.Text, nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    company = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    is_read = db.Column(db.Boolean, default=False, nullable=False)
    
    def __repr__(self):
        return f'<Contact {self.name} - {self.email}>'
    
    def to_dict(self):
        """Convert contact object to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'subject': self.subject,
            'message': self.message,
            'phone': self.phone,
            'company': self.company,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'is_read': self.is_read
        }

class Newsletter(db.Model):
    """Model for newsletter subscriptions"""
    
    __tablename__ = 'newsletter_subscriptions'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    subscribed_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    
    def __repr__(self):
        return f'<Newsletter {self.email}>'
    
    def to_dict(self):
        """Convert newsletter subscription to dictionary"""
        return {
            'id': self.id,
            'email': self.email,
            'subscribed_at': self.subscribed_at.isoformat() if self.subscribed_at else None,
            'is_active': self.is_active
        }
