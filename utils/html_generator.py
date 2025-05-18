import os
import re
from bs4 import BeautifulSoup
import logging

def generate_blog_template(analysis_result, css_filename, js_filename):
    """
    Generate a blog homepage template based on the website analysis.
    
    Args:
        analysis_result: The result of the website analysis
        css_filename: The filename of the hosted CSS file
        js_filename: The filename of the hosted JS file
        
    Returns:
        The HTML template as a string
    """
    try:
        # Extract style information from the analysis result
        colors = analysis_result.get('colors', {})
        typography = analysis_result.get('typography', {})
        layout = analysis_result.get('layout', {})
        components = analysis_result.get('components', {})
        business = analysis_result.get('business', {})
        
        # Create the HTML template
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{business.get('name', 'Blog')} - Blog</title>
    <meta name="description" content="The official blog for {business.get('name', 'our website')}">
    <link rel="stylesheet" href="https://ourdomain.com/cssstyles/{css_filename}">
    <script src="https://ourdomain.com/scripts/{js_filename}" defer></script>
</head>
<body>
    <header class="blog-header">
        <div class="container">
            <div class="blog-header-content">
                <h1 class="blog-title">{business.get('name', 'Our')} Blog</h1>
                <nav class="blog-nav">
                    <ul>
                        <li><a href="../index.html">Home</a></li>
                        <li><a href="blog.html" class="active">Blog</a></li>
                    </ul>
                </nav>
            </div>
        </div>
    </header>

    <main class="blog-main">
        <div class="container">
            <section class="blog-posts">
                <h2>Latest Posts</h2>
                
                <!-- BLOG_POSTS_PLACEHOLDER -->
                
            </section>
        </div>
    </main>

    <footer class="blog-footer">
        <div class="container">
            <p>&copy; {business.get('name', 'Website')} - All rights reserved</p>
        </div>
    </footer>
</body>
</html>"""
        
        return html
    
    except Exception as e:
        logging.error(f"Error generating blog template: {str(e)}")
        # Return a simple default template
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Blog</title>
    <meta name="description" content="Our Blog">
    <link rel="stylesheet" href="https://ourdomain.com/cssstyles/{css_filename}">
    <script src="https://ourdomain.com/scripts/{js_filename}" defer></script>
</head>
<body>
    <header>
        <div class="container">
            <h1>Our Blog</h1>
            <nav>
                <ul>
                    <li><a href="../index.html">Home</a></li>
                    <li><a href="blog.html">Blog</a></li>
                </ul>
            </nav>
        </div>
    </header>

    <main>
        <div class="container">
            <section>
                <h2>Latest Posts</h2>
                
                <!-- BLOG_POSTS_PLACEHOLDER -->
                
            </section>
        </div>
    </main>

    <footer>
        <div class="container">
            <p>&copy; Website - All rights reserved</p>
        </div>
    </footer>
</body>
</html>"""

def generate_post_template(analysis_result, css_filename, js_filename):
    """
    Generate a blog post template based on the website analysis.
    
    Args:
        analysis_result: The result of the website analysis
        css_filename: The filename of the hosted CSS file
        js_filename: The filename of the hosted JS file
        
    Returns:
        The HTML template as a string
    """
    try:
        # Extract style information from the analysis result
        colors = analysis_result.get('colors', {})
        typography = analysis_result.get('typography', {})
        layout = analysis_result.get('layout', {})
        components = analysis_result.get('components', {})
        business = analysis_result.get('business', {})
        
        # Create the HTML template
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{POST_TITLE}} - {business.get('name', 'Blog')}</title>
    <meta name="description" content="{{POST_META_DESCRIPTION}}">
    <link rel="stylesheet" href="https://ourdomain.com/cssstyles/{css_filename}">
    <script src="https://ourdomain.com/scripts/{js_filename}" defer></script>
</head>
<body>
    <header class="blog-header">
        <div class="container">
            <div class="blog-header-content">
                <h1 class="blog-title">{business.get('name', 'Our')} Blog</h1>
                <nav class="blog-nav">
                    <ul>
                        <li><a href="../../index.html">Home</a></li>
                        <li><a href="../blog.html">Blog</a></li>
                    </ul>
                </nav>
            </div>
        </div>
    </header>

    <main class="blog-main">
        <div class="container">
            <article class="blog-post">
                <header class="post-header">
                    <h1 class="post-title">{{POST_TITLE}}</h1>
                    <div class="post-meta">
                        <time datetime="{{POST_DATE}}">{{POST_DATE_FORMATTED}}</time>
                    </div>
                </header>
                
                <div class="post-content">
                    {{POST_CONTENT}}
                </div>
                
                <div class="post-cta">
                    <h3>Ready to get started?</h3>
                    <p>Check out {business.get('name', 'our website')} and see how we can help you.</p>
                    <a href="../../index.html" class="btn btn-primary">Learn More</a>
                </div>
            </article>
        </div>
    </main>

    <footer class="blog-footer">
        <div class="container">
            <p>&copy; {business.get('name', 'Website')} - All rights reserved</p>
        </div>
    </footer>
</body>
</html>"""
        
        return html
    
    except Exception as e:
        logging.error(f"Error generating post template: {str(e)}")
        # Return a simple default template
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{POST_TITLE}} - Blog</title>
    <meta name="description" content="{{POST_META_DESCRIPTION}}">
    <link rel="stylesheet" href="https://ourdomain.com/cssstyles/{css_filename}">
    <script src="https://ourdomain.com/scripts/{js_filename}" defer></script>
</head>
<body>
    <header>
        <div class="container">
            <h1>Our Blog</h1>
            <nav>
                <ul>
                    <li><a href="../../index.html">Home</a></li>
                    <li><a href="../blog.html">Blog</a></li>
                </ul>
            </nav>
        </div>
    </header>

    <main>
        <div class="container">
            <article>
                <header>
                    <h1>{{POST_TITLE}}</h1>
                    <div>
                        <time datetime="{{POST_DATE}}">{{POST_DATE_FORMATTED}}</time>
                    </div>
                </header>
                
                <div>
                    {{POST_CONTENT}}
                </div>
                
                <div>
                    <h3>Ready to get started?</h3>
                    <p>Check out our website and see how we can help you.</p>
                    <a href="../../index.html" class="btn btn-primary">Learn More</a>
                </div>
            </article>
        </div>
    </main>

    <footer>
        <div class="container">
            <p>&copy; Website - All rights reserved</p>
        </div>
    </footer>
</body>
</html>"""
