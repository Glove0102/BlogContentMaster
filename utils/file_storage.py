
import os
import io
import uuid
import time
import zipfile
import logging
import re
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
                    post_date = post.created_at.strftime("%B %d, %Y") if hasattr(post, 'created_at') else ""
                    post_links += f'''
                    <div class="blog-post-card">
                        <h3><a href="posts/{post.id}.html">{post.title}</a></h3>
                        <p class="post-date">{post_date}</p>
                        <p class="post-excerpt">{post.meta_description if post.meta_description else ''}</p>
                        <a href="posts/{post.id}.html" class="btn">Read More</a>
                    </div>
                    '''
                
                # Replace placeholder with actual post links
                blog_html = blog_html.replace('<!-- BLOG_POSTS_PLACEHOLDER -->', post_links)
                
                # Fix the CSS and JS links to use local paths
                blog_html = blog_html.replace(f'https://ourdomain.com/cssstyles/{project.hosted_css_filename}', 'assets/css/blog-styles.css')
                if project.hosted_js_filename:
                    blog_html = blog_html.replace(f'https://ourdomain.com/scripts/{project.hosted_js_filename}', 'assets/js/blog-scripts.js')
                
                # Add the file to the ZIP
                zf.writestr('blog/blog.html', blog_html)
            
            # Create posts directory and add blog posts
            if blog_posts:
                # Add each blog post as an HTML file
                for post in blog_posts:
                    # Check if we have a complete HTML document or just content fragment
                    if post.html_content and ('<html' in post.html_content):
                        post_html = post.html_content
                        
                        # Fix the CSS and JS links to use local paths
                        post_html = post_html.replace(f'https://ourdomain.com/cssstyles/{project.hosted_css_filename}', '../assets/css/blog-styles.css')
                        if project.hosted_js_filename:
                            post_html = post_html.replace(f'https://ourdomain.com/scripts/{project.hosted_js_filename}', '../assets/js/blog-scripts.js')
                    else:
                        # We have just the content fragment, not a complete document
                        # Use the post template to create a complete HTML document
                        if project.post_template_html:
                            post_date = post.created_at.strftime("%B %d, %Y") if hasattr(post, 'created_at') else ""
                            meta_desc = post.meta_description if post.meta_description else f"Read our blog post about {post.title}"
                            
                            # Start with the template
                            post_html = project.post_template_html
                            
                            # Replace placeholder values with actual content
                            post_html = post_html.replace("{{title}}", post.title)
                            post_html = post_html.replace("{{meta_description}}", meta_desc)
                            post_html = post_html.replace("{{post_date}}", post_date)
                            post_html = post_html.replace("{{content}}", post.html_content or post.content)
                            
                            # Fix the CSS and JS links to use local paths
                            post_html = post_html.replace(f'https://ourdomain.com/cssstyles/{project.hosted_css_filename}', '../assets/css/blog-styles.css')
                            if project.hosted_js_filename:
                                post_html = post_html.replace(f'https://ourdomain.com/scripts/{project.hosted_js_filename}', '../assets/js/blog-scripts.js')
                        else:
                            # Fallback to basic HTML if no template is available
                            post_date = post.created_at.strftime("%B %d, %Y") if hasattr(post, 'created_at') else ""
                            post_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{post.title}</title>
    <link rel="stylesheet" href="../assets/css/blog-styles.css">
</head>
<body>
    <header class="site-header">
        <div class="container">
            <h1 class="site-title">{project.name} Blog</h1>
            <nav class="site-navigation">
                <a href="../index.html">Home</a>
                <a href="../blog.html">Blog</a>
            </nav>
        </div>
    </header>

    <main class="container">
        <article class="blog-post">
            <h1 class="post-title">{post.title}</h1>
            <div class="post-meta">Published on {post_date}</div>
            <div class="post-content">
                {post.html_content or post.content}
            </div>
        </article>
    </main>

    <footer class="site-footer">
        <div class="container">
            <p>&copy; {datetime.now().year} - All rights reserved</p>
        </div>
    </footer>
</body>
</html>"""
                    
                    # Write the post HTML to the ZIP file
                    zf.writestr(f'blog/posts/{post.id}.html', post_html)
            
            # Create assets directories
            zf.writestr('blog/posts/.keep', '')
            zf.writestr('blog/assets/images/.keep', '')
            
            # Create css directory and add CSS file
            css_content = ""
            
            # Start with original CSS if available
            if project.css_file_path and os.path.exists(project.css_file_path):
                try:
                    with open(project.css_file_path, 'r', encoding='utf-8') as css_file:
                        css_content = css_file.read()
                except:
                    pass
            
            # Add hosted CSS if available 
            if project.hosted_css_filename:
                css_path = os.path.join(app.config.get('HOSTED_FILES_FOLDER', 'static/hosted_files'), 'cssstyles', project.hosted_css_filename)
                if os.path.exists(css_path):
                    try:
                        with open(css_path, 'r', encoding='utf-8') as css_file:
                            hosted_css = css_file.read()
                            if hosted_css and not css_content:
                                css_content = hosted_css
                            elif hosted_css:
                                css_content += "\n\n/* Additional styles */\n" + hosted_css
                    except:
                        pass
            
            # Extract custom CSS from template
            if project.blog_template_html:
                css_match = re.search(r'<style>(.*?)</style>', project.blog_template_html, re.DOTALL)
                if css_match:
                    custom_css = css_match.group(1)
                    if custom_css:
                        css_content += "\n\n/* Custom blog styles */\n" + custom_css
            
            zf.writestr('blog/assets/css/blog-styles.css', css_content)
            
            # Create js directory and add JS file
            js_content = ""
            if project.hosted_js_filename:
                js_path = os.path.join(app.config.get('HOSTED_FILES_FOLDER', 'static/hosted_files'), 'scripts', project.hosted_js_filename)
                if os.path.exists(js_path):
                    try:
                        with open(js_path, 'r', encoding='utf-8') as js_file:
                            js_content = js_file.read()
                    except:
                        pass
            
            zf.writestr('blog/assets/js/blog-scripts.js', js_content)
            
            # Add a README file
            readme_content = f"""# {project.name} Blog

This package contains a complete blog for your website. Here's how to use it:

1. Upload the entire 'blog' folder to your website
2. The main blog page is at 'blog/blog.html'
3. Individual blog posts are in the 'blog/posts/' directory
4. The CSS and JS files are included in the assets folder:
   - CSS: blog/assets/css/blog-styles.css
   - JS: blog/assets/js/blog-scripts.js

All files are already properly linked in the HTML files.

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
