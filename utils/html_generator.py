import re
import logging
from bs4 import BeautifulSoup
from datetime import datetime

def generate_blog_template(analysis_result, css_filename, js_filename):
    """Generate a blog homepage template based on website analysis"""
    try:
        # Extract style information
        colors = analysis_result.get('colors', {})
        typography = analysis_result.get('typography', {})
        layout = analysis_result.get('layout', {})
        components = analysis_result.get('components', {})
        business = analysis_result.get('business', {})
        
        # Use standard styling based on the project's index.css
        primary_color = colors.get('primary', '#007bff')
        secondary_color = colors.get('secondary', '#6c757d')
        background_color = colors.get('background', '#ffffff')
        text_color = colors.get('text', '#333333')
        accent_color = colors.get('accent', '#17a2b8')
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{business.get('name', 'Blog')} - Blog</title>
    <meta name="description" content="The official blog for {business.get('name', 'our website')}">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        :root {{
            --primary-color: {primary_color};
            --secondary-color: {secondary_color};
            --background-color: {background_color};
            --text-color: {text_color};
            --accent-color: {accent_color};
        }}
        
        body {{
            font-family: 'Arial', sans-serif;
            color: var(--text-color);
            background-color: var(--background-color);
            line-height: 1.6;
            margin: 0;
            padding: 0;
        }}
        
        .header {{
            background-color: var(--primary-color);
            color: white;
            padding: 2rem 0;
            margin-bottom: 2rem;
        }}
        
        .blog-title {{
            font-weight: bold;
        }}
        
        .blog-card {{
            border: 1px solid #eee;
            border-radius: 0.5rem;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        
        .blog-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
        }}
        
        .footer {{
            background-color: #f8f9fa;
            padding: 2rem 0;
            margin-top: 3rem;
            border-top: 1px solid #eee;
        }}
    </style>
</head>
<body>
    <header class="header">
        <div class="container">
            <h1 class="blog-title">{business.get('name', 'Our')} Blog</h1>
            <nav class="mt-3">
                <ul class="nav">
                    <li class="nav-item"><a class="nav-link text-white" href="../index.html">Home</a></li>
                    <li class="nav-item"><a class="nav-link text-white" href="blog.html">Blog</a></li>
                </ul>
            </nav>
        </div>
    </header>

    <main class="container">
        <section>
            <h2 class="mb-4">Latest Posts</h2>
            
            <!-- BLOG_POSTS_PLACEHOLDER -->
            
        </section>
    </main>

    <footer class="footer">
        <div class="container text-center">
            <p>&copy; {business.get('name', 'Website')} - All rights reserved</p>
        </div>
    </footer>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>"""
        return html
    
    except Exception as e:
        logging.error(f"Error generating blog template: {str(e)}")
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Blog</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <header class="bg-primary text-white py-4">
        <div class="container">
            <h1>Our Blog</h1>
            <nav class="mt-2">
                <ul class="nav">
                    <li class="nav-item"><a class="nav-link text-white" href="../index.html">Home</a></li>
                    <li class="nav-item"><a class="nav-link text-white" href="blog.html">Blog</a></li>
                </ul>
            </nav>
        </div>
    </header>

    <main class="container py-4">
        <section>
            <h2 class="mb-4">Latest Posts</h2>
            
            <!-- BLOG_POSTS_PLACEHOLDER -->
            
        </section>
    </main>

    <footer class="bg-light py-4 mt-5">
        <div class="container text-center">
            <p>&copy; Website - All rights reserved</p>
        </div>
    </footer>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>"""

def generate_post_template(analysis_result, css_filename, js_filename, title="", content="", meta_description=""):
    """
    Generate a blog post template based on the website analysis.
    
    Args:
        analysis_result: The result of the website analysis
        css_filename: The filename of the hosted CSS file
        js_filename: The filename of the hosted JS file
        title: The blog post title (optional)
        content: The blog post content (optional)
        meta_description: The meta description for the post (optional)
        
    Returns:
        The HTML template as a string
    """
    try:
        # Extract style information
        colors = analysis_result.get('colors', {})
        typography = analysis_result.get('typography', {})
        layout = analysis_result.get('layout', {})
        components = analysis_result.get('components', {})
        business = analysis_result.get('business', {})
        
        # Use standard styling based on the project's index.css
        primary_color = colors.get('primary', '#007bff')
        secondary_color = colors.get('secondary', '#6c757d')
        background_color = colors.get('background', '#ffffff')
        text_color = colors.get('text', '#333333')
        accent_color = colors.get('accent', '#17a2b8')
        
        template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{title}} - {business.get('name', 'Blog')}</title>
    <meta name="description" content="{{meta_description}}">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        :root {{
            --primary-color: {primary_color};
            --secondary-color: {secondary_color};
            --background-color: {background_color};
            --text-color: {text_color};
            --accent-color: {accent_color};
        }}
        
        body {{
            font-family: 'Arial', sans-serif;
            color: var(--text-color);
            background-color: var(--background-color);
            line-height: 1.6;
        }}
        
        .header {{
            background-color: var(--primary-color);
            color: white;
            padding: 2rem 0;
            margin-bottom: 2rem;
        }}
        
        .post-title {{
            font-weight: bold;
            margin-bottom: 1rem;
        }}
        
        .post-meta {{
            color: #6c757d;
            margin-bottom: 2rem;
        }}
        
        .post-content {{
            margin-bottom: 3rem;
        }}
        
        .post-content img {{
            max-width: 100%;
            height: auto;
            margin-bottom: 1.5rem;
        }}
        
        .post-content h2 {{
            margin-top: 2rem;
            margin-bottom: 1rem;
        }}
        
        .post-content p {{
            margin-bottom: 1.5rem;
        }}
        
        .footer {{
            background-color: #f8f9fa;
            padding: 2rem 0;
            margin-top: 3rem;
            border-top: 1px solid #eee;
        }}
    </style>
</head>
<body>
    <header class="header">
        <div class="container">
            <h1 class="blog-title">{business.get('name', 'Our')} Blog</h1>
            <nav class="mt-3">
                <ul class="nav">
                    <li class="nav-item"><a class="nav-link text-white" href="../index.html">Home</a></li>
                    <li class="nav-item"><a class="nav-link text-white" href="blog.html">Blog</a></li>
                </ul>
            </nav>
        </div>
    </header>

    <main class="container">
        <article>
            <h1 class="post-title">{{title}}</h1>
            <div class="post-meta">Published on {{post_date}}</div>
            
            <div class="post-content">
                {{content}}
            </div>
        </article>
    </main>

    <footer class="footer">
        <div class="container text-center">
            <p>&copy; {business.get('name', 'Website')} - All rights reserved</p>
        </div>
    </footer>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>"""
        return template
        
    except Exception as e:
        logging.error(f"Error generating post template: {str(e)}")
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{title}} - Blog</title>
    <meta name="description" content="{{meta_description}}">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <header class="bg-primary text-white py-4">
        <div class="container">
            <h1>Our Blog</h1>
            <nav class="mt-2">
                <ul class="nav">
                    <li class="nav-item"><a class="nav-link text-white" href="../index.html">Home</a></li>
                    <li class="nav-item"><a class="nav-link text-white" href="blog.html">Blog</a></li>
                </ul>
            </nav>
        </div>
    </header>

    <main class="container py-4">
        <article>
            <h1 class="mb-3">{{title}}</h1>
            <div class="text-muted mb-4">Published on {{post_date}}</div>
            
            <div class="post-content">
                {{content}}
            </div>
        </article>
    </main>

    <footer class="bg-light py-4 mt-5">
        <div class="container text-center">
            <p>&copy; Website - All rights reserved</p>
        </div>
    </footer>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>"""

def format_blog_html(title, content, style_analysis):
    """
    Format blog content as HTML based on the website's style.
    
    Args:
        title: The blog post title
        content: The blog post content
        style_analysis: Analysis of the website's style
        
    Returns:
        Formatted HTML content
    """
    try:
        # Parse the markdown-like content
        html_content = ""
        
        # Split content into paragraphs
        paragraphs = content.split("\n\n")
        
        for paragraph in paragraphs:
            # Check if it's a heading
            if paragraph.startswith("# "):
                html_content += f"<h2>{paragraph[2:]}</h2>\n"
            elif paragraph.startswith("## "):
                html_content += f"<h3>{paragraph[3:]}</h3>\n"
            elif paragraph.startswith("### "):
                html_content += f"<h4>{paragraph[4:]}</h4>\n"
            # Check if it's a list item
            elif paragraph.startswith("- "):
                items = paragraph.split("\n")
                html_content += "<ul>\n"
                for item in items:
                    if item.startswith("- "):
                        html_content += f"<li>{item[2:]}</li>\n"
                html_content += "</ul>\n"
            # Regular paragraph
            else:
                html_content += f"<p>{paragraph}</p>\n"
        
        return html_content
        
    except Exception as e:
        logging.error(f"Error formatting blog HTML: {str(e)}")
        return f"<p>{content}</p>"