import os
import json
import uuid
import time
import logging
from datetime import datetime
from flask import render_template, request, redirect, url_for, session, flash, jsonify, send_file
from flask_login import current_user
from werkzeug.utils import secure_filename
from app import app, db
from models import Project, BlogPost
from replit_auth import require_login, make_replit_blueprint
from utils.html_analyzer import analyze_html_css
from utils.file_storage import save_uploaded_file, generate_unique_filename, create_download_package
from utils.html_generator import generate_blog_template, generate_post_template
from openai_service import generate_blog_content, analyze_website_content
import io
import zipfile

# Register Replit Auth Blueprint
app.register_blueprint(make_replit_blueprint(), url_prefix="/auth")

# Make session permanent
@app.before_request
def make_session_permanent():
    session.permanent = True

# Landing Page
@app.route('/')
def index():
    return render_template('index.html', user=current_user)

# Dashboard - List all projects
@app.route('/dashboard')
@require_login
def dashboard():
    projects = Project.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', user=current_user, projects=projects)

# Create new project
@app.route('/projects/new', methods=['POST'])
@require_login
def create_project():
    name = request.form.get('name')
    description = request.form.get('description', '')
    
    if not name:
        flash('Project name is required', 'danger')
        return redirect(url_for('dashboard'))
    
    project = Project(
        name=name,
        description=description,
        user_id=current_user.id
    )
    db.session.add(project)
    db.session.commit()
    
    flash('Project created successfully!', 'success')
    return redirect(url_for('project_detail', project_id=project.id))

# Project detail page
@app.route('/projects/<int:project_id>')
@require_login
def project_detail(project_id):
    project = Project.query.filter_by(id=project_id, user_id=current_user.id).first_or_404()
    blog_posts = BlogPost.query.filter_by(project_id=project_id).all()
    return render_template('project.html', project=project, blog_posts=blog_posts)

# Upload website files
@app.route('/projects/<int:project_id>/upload', methods=['POST'])
@require_login
def upload_files(project_id):
    project = Project.query.filter_by(id=project_id, user_id=current_user.id).first_or_404()
    
    # Check if files were uploaded
    if 'html_file' not in request.files or 'css_file' not in request.files:
        flash('Both HTML and CSS files are required', 'danger')
        return redirect(url_for('project_detail', project_id=project_id))
    
    html_file = request.files['html_file']
    css_file = request.files['css_file']
    website_purpose = request.form.get('website_purpose', '')
    
    # Check if filenames are valid
    if html_file.filename == '' or css_file.filename == '':
        flash('Both HTML and CSS files are required', 'danger')
        return redirect(url_for('project_detail', project_id=project_id))
    
    # Save HTML file
    html_path = save_uploaded_file(html_file, 'html')
    
    # Save CSS file
    css_path = save_uploaded_file(css_file, 'css')
    
    # Update project with file paths and website purpose
    project.html_file_path = html_path
    project.css_file_path = css_path
    project.website_purpose = website_purpose
    
    # Analyze the website content and style
    analysis_result = analyze_html_css(html_path, css_path)
    
    # Use OpenAI to enhance the analysis
    website_analysis = analyze_website_content(
        html_path=html_path, 
        css_path=css_path, 
        website_purpose=website_purpose
    )
    
    # Generate unique filenames for hosted CSS and JS
    timestamp = int(time.time())
    css_filename = f"{project.id}_{timestamp}.css"
    js_filename = f"{project.id}_{timestamp}.js"
    
    # Save hosted filenames
    project.hosted_css_filename = css_filename
    project.hosted_js_filename = js_filename
    
    # Copy CSS file to hosted directory
    from utils.file_storage import copy_css_to_hosted
    hosted_css_path = copy_css_to_hosted(css_path, css_filename)
    
    # Merge analysis results
    project.style_analysis = {
        **analysis_result,
        **website_analysis
    }
    
    # Generate blog and post templates
    blog_template = generate_blog_template(
        analysis_result=project.style_analysis,
        css_filename=css_filename,
        js_filename=js_filename
    )
    
    post_template = generate_post_template(
        analysis_result=project.style_analysis,
        css_filename=css_filename,
        js_filename=js_filename
    )
    
    # Save templates
    project.blog_template_html = blog_template
    project.post_template_html = post_template
    
    db.session.commit()
    
    flash('Website files uploaded and analyzed successfully!', 'success')
    return redirect(url_for('project_detail', project_id=project_id))

# Create a new blog post
@app.route('/projects/<int:project_id>/posts/new', methods=['GET', 'POST'])
@require_login
def create_post(project_id):
    project = Project.query.filter_by(id=project_id, user_id=current_user.id).first_or_404()
    
    if request.method == 'POST':
        # Get form data
        title = request.form.get('title')
        topic_input = request.form.get('topic_input')
        inspiration_url = request.form.get('inspiration_url')
        
        # Require either topic or URL inspiration
        if not topic_input and not inspiration_url:
            flash('Please provide either a topic or URL inspiration to generate content', 'danger')
            return redirect(url_for('create_post', project_id=project_id))
        
        # If no title is provided, generate one based on topic or URL
        if not title:
            # First, attempt to generate a title
            from openai_service import generate_blog_title
            generated_title = generate_blog_title(
                topic=topic_input,
                inspiration_url=inspiration_url,
                website_info=project.website_purpose
            )
            title = generated_title
        
        # Generate blog post content
        content_result = generate_blog_content(
            title=title,
            topic=topic_input,
            inspiration_url=inspiration_url,
            website_info=project.website_purpose,
            style_analysis=project.style_analysis
        )
        
        # Create blog post
        blog_post = BlogPost(
            title=title,
            content=content_result['content'],
            meta_description=content_result.get('meta_description', ''),
            html_content=content_result['formatted_html'],
            project_id=project_id
        )
        
        db.session.add(blog_post)
        db.session.commit()
        
        flash('Blog post created successfully!', 'success')
        return redirect(url_for('project_detail', project_id=project_id))
    
    return render_template('content.html', project=project)

# Preview blog post
@app.route('/posts/<int:post_id>/preview')
@require_login
def preview_post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    project = Project.query.filter_by(id=post.project_id, user_id=current_user.id).first_or_404()
    
    return render_template('preview.html', post=post, project=project)

# Edit blog post
@app.route('/posts/<int:post_id>/edit', methods=['GET', 'POST'])
@require_login
def edit_post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    project = Project.query.filter_by(id=post.project_id, user_id=current_user.id).first_or_404()
    
    if request.method == 'POST':
        post.title = request.form.get('title')
        post.content = request.form.get('content')
        post.meta_description = request.form.get('meta_description', '')
        
        # Update HTML content
        updated_content_result = generate_blog_content(
            title=post.title,
            content=post.content,  # Use existing content
            website_info=project.website_purpose,
            style_analysis=project.style_analysis
        )
        
        post.html_content = updated_content_result['formatted_html']
        db.session.commit()
        
        flash('Blog post updated successfully!', 'success')
        return redirect(url_for('project_detail', project_id=project.id))
    
    return render_template('content.html', project=project, post=post, edit_mode=True)

# Delete blog post
@app.route('/posts/<int:post_id>/delete', methods=['POST'])
@require_login
def delete_post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    project = Project.query.filter_by(id=post.project_id, user_id=current_user.id).first_or_404()
    
    db.session.delete(post)
    db.session.commit()
    
    flash('Blog post deleted successfully!', 'success')
    return redirect(url_for('project_detail', project_id=project.id))

# Edit blog CSS
@app.route('/projects/<int:project_id>/edit-css', methods=['GET', 'POST'])
@require_login
def edit_blog_css(project_id):
    project = Project.query.filter_by(id=project_id, user_id=current_user.id).first_or_404()
    
    # Make sure the project has a CSS file
    if not project.hosted_css_filename:
        flash('No CSS file found for this project', 'danger')
        return redirect(url_for('project_detail', project_id=project_id))
    
    # Get the path to the CSS file
    css_path = os.path.join(app.config['HOSTED_FILES_FOLDER'], 'cssstyles', project.hosted_css_filename)
    
    if request.method == 'POST':
        # Get the updated CSS content
        css_content = request.form.get('css_content')
        
        # Save the updated CSS content
        try:
            # Ensure css_content is not None
            if css_content is None:
                css_content = ""
                
            with open(css_path, 'w', encoding='utf-8') as f:
                f.write(css_content)
            
            flash('CSS file updated successfully', 'success')
            return redirect(url_for('project_detail', project_id=project_id))
        except Exception as e:
            logging.error(f"Error saving CSS file: {str(e)}")
            flash('Error saving CSS file', 'danger')
    
    # Read the current CSS content for the form
    css_content = ""
    try:
        with open(css_path, 'r', encoding='utf-8') as f:
            css_content = f.read()
    except Exception as e:
        logging.error(f"Error reading CSS file: {str(e)}")
        flash('Error reading CSS file', 'danger')
    
    return render_template('edit_css.html', project=project, css_content=css_content)

# Export blog package
@app.route('/projects/<int:project_id>/export')
@require_login
def export_project(project_id):
    project = Project.query.filter_by(id=project_id, user_id=current_user.id).first_or_404()
    blog_posts = BlogPost.query.filter_by(project_id=project_id).all()
    
    # Create a download package
    zip_data = create_download_package(project, blog_posts)
    
    # Return the zip file
    return send_file(
        io.BytesIO(zip_data),
        mimetype='application/zip',
        as_attachment=True,
        download_name=f"{project.name}_blog_export.zip"
    )

# 403 Error handler
@app.errorhandler(403)
def forbidden(error):
    return render_template('403.html'), 403
