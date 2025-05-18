from datetime import datetime
from app import db
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin
from flask_login import UserMixin
from sqlalchemy import UniqueConstraint, ForeignKey, Text

# User model for Replit Auth
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=True)
    first_name = db.Column(db.String, nullable=True)
    last_name = db.Column(db.String, nullable=True)
    profile_image_url = db.Column(db.String, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relationship with projects
    projects = db.relationship('Project', backref='user', lazy=True, cascade="all, delete-orphan")

# OAuth model for Replit Auth
class OAuth(OAuthConsumerMixin, db.Model):
    user_id = db.Column(db.String, db.ForeignKey(User.id))
    browser_session_key = db.Column(db.String, nullable=False)
    user = db.relationship(User)

    __table_args__ = (UniqueConstraint(
        'user_id',
        'browser_session_key',
        'provider',
        name='uq_user_browser_session_key_provider',
    ),)

# Project model to store user website projects
class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.String, db.ForeignKey(User.id), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Website details
    html_file_path = db.Column(db.String, nullable=True)
    css_file_path = db.Column(db.String, nullable=True)
    website_purpose = db.Column(db.Text, nullable=True)
    
    # Style analysis results
    style_analysis = db.Column(db.JSON, nullable=True)
    
    # Hosted files
    hosted_css_filename = db.Column(db.String, nullable=True)
    hosted_js_filename = db.Column(db.String, nullable=True)
    
    # Template info
    blog_template_html = db.Column(db.Text, nullable=True)
    post_template_html = db.Column(db.Text, nullable=True)
    
    # Relationships
    blog_posts = db.relationship('BlogPost', backref='project', lazy=True, cascade="all, delete-orphan")

# BlogPost model to store generated blog posts
class BlogPost(db.Model):
    __tablename__ = 'blog_posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    meta_description = db.Column(db.String(255), nullable=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    html_content = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
