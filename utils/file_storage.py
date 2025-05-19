
import os
import io
import uuid
import time
import zipfile
import logging
from werkzeug.utils import secure_filename
from app import app
from flask import url_for, request

def save_uploaded_file(file, file_type):
    """
    Save an uploaded file to the uploads directory.
    
    Args:
        file: The uploaded file object
        file_type: The type of file (html, css, etc.)
        
    Returns:
        The path to the saved file
    """
    try:
        # Create a secure filename
        filename = secure_filename(file.filename)
        
        # Add a timestamp and unique ID to avoid overwriting files
        unique_filename = f"{int(time.time())}_{uuid.uuid4().hex}_{filename}"
        
        # Create the full path
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        
        # Save the file
        file.save(file_path)
        
        return file_path
    
    except Exception as e:
        logging.error(f"Error saving uploaded file: {str(e)}")
        raise e

def generate_unique_filename(project_id, original_filename, file_type):
    """
    Generate a unique filename for a hosted file.
    
    Args:
        project_id: The ID of the project
        original_filename: The original filename
        file_type: The type of file (css, js)
        
    Returns:
        The unique filename
    """
    timestamp = int(time.time())
    ext = os.path.splitext(original_filename)[1] if '.' in original_filename else f".{file_type}"
    
    return f"{project_id}_{timestamp}{ext}"

def save_hosted_file(content, filename, file_type):
    """
    Save a file to the hosted files directory.
    
    Args:
        content: The content of the file
        filename: The filename
        file_type: The type of file (css, js)
        
    Returns:
        The URL to the hosted file
    """
    try:
        # Determine the correct folder
        if file_type == 'css':
            folder = 'cssstyles'
        elif file_type == 'js':
            folder = 'scripts'
        else:
            raise ValueError(f"Unsupported file type: {file_type}")
        
        # Create the full path
        file_path = os.path.join(app.config['HOSTED_FILES_FOLDER'], folder, filename)
        
        # Save the file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Return the URL
        return f"https://{request.host}/hosted_files/{folder}/{filename}"
    
    except Exception as e:
        logging.error(f"Error saving hosted file: {str(e)}")
        raise e

def copy_css_to_hosted(css_file_path, hosted_css_filename):
    """
    Copy a CSS file from uploads to the hosted_files/cssstyles directory.
    
    Args:
        css_file_path: The path to the source CSS file
        hosted_css_filename: The filename for the hosted CSS file
        
    Returns:
        The full path to the hosted CSS file
    """
    try:
        # Create the full path for the hosted CSS file
        hosted_css_path = os.path.join(app.config['HOSTED_FILES_FOLDER'], 'cssstyles', hosted_css_filename)
        
        # Read the original CSS file
        with open(css_file_path, 'r', encoding='utf-8') as source_file:
            css_content = source_file.read()
        
        # Write to the hosted CSS file
        with open(hosted_css_path, 'w', encoding='utf-8') as dest_file:
            dest_file.write(css_content)
        
        return hosted_css_path
    
    except Exception as e:
        logging.error(f"Error copying CSS to hosted directory: {str(e)}")
        raise e

def create_download_package(project, blog_posts):
    """
    Create a downloadable ZIP package containing the blog files.
    
    Args:
        project: The project object
        blog_posts: List of blog post objects
        
    Returns:
        The ZIP file as bytes
    """
    try:
        # Create a memory file for the ZIP
        memory_file = io.BytesIO()
        
        # Create a ZIP file
        with zipfile.ZipFile(memory_file, 'w') as zf:
            # Add the blog.html file
            if project.blog_template_html:
                # Prepare the blog homepage
                blog_html = project.blog_template_html
                
                # Add links to blog posts
                post_links = ""
                for post in blog_posts:
                    post_links += f'<div class="blog-post-card"><h3><a href="posts/{post.id}.html">{post.title}</a></h3></div>\n'
                
                # Replace placeholder with actual post links
                blog_html = blog_html.replace('<!-- BLOG_POSTS_PLACEHOLDER -->', post_links)
                
                # Add the file to the ZIP
                zf.writestr('blog/blog.html', blog_html)
            
            # Create posts directory
            if blog_posts:
                # Add each blog post as an HTML file
                for post in blog_posts:
                    post_html = post.html_content
                    zf.writestr(f'blog/posts/{post.id}.html', post_html)
            
            # Create empty directories
            zf.writestr('blog/posts/.keep', '')
            zf.writestr('blog/assets/images/.keep', '')
            
            # Add a README file
            readme_content = f"""# {project.name} Blog

This package contains a blog for your website. Here's how to use it:

1. Upload the entire 'blog' folder to your website
2. The main blog page is at 'blog/blog.html'
3. Individual blog posts are in the 'blog/posts/' directory
4. The CSS and JS files are hosted at:
   - CSS: https://ourdomain.com/cssstyles/{project.hosted_css_filename}
   - JS: https://ourdomain.com/scripts/{project.hosted_js_filename}

These files are already referenced in the HTML files.

Enjoy your new blog!
"""
            zf.writestr('README.md', readme_content)
        
        # Reset the file pointer
        memory_file.seek(0)
        
        # Return the ZIP file
        return memory_file.getvalue()
    
    except Exception as e:
        logging.error(f"Error creating download package: {str(e)}")
        raise e
