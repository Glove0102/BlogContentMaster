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
        
        # Extract font families and sizes from typography
        heading_font = typography.get('headingFont', 'sans-serif')
        body_font = typography.get('bodyFont', 'sans-serif')
        h1_size = typography.get('headingSizes', {}).get('h1', '2rem')
        h2_size = typography.get('headingSizes', {}).get('h2', '1.75rem')
        h3_size = typography.get('headingSizes', {}).get('h3', '1.5rem')
        body_size = typography.get('bodySize', '1rem')
        
        # Extract colors
        primary_color = colors.get('primary', '#007bff')
        secondary_color = colors.get('secondary', '#6c757d')
        background_color = colors.get('background', '#ffffff')
        text_color = colors.get('text', '#333333')
        accent_color = colors.get('accent', '#17a2b8')
        
        # Extract layout information
        container_width = layout.get('containerWidth', '1200px')
        spacing = layout.get('spacing', '1rem')
        header_style = layout.get('headerStyle', 'Simple header with logo and navigation')
        footer_style = layout.get('footerStyle', 'Basic footer with copyright information')
        
        # Extract component styles
        button_style = components.get('buttonStyle', 'Standard rounded buttons with hover effect')
        link_style = components.get('linkStyle', 'Underlined links with color change on hover')
        card_style = components.get('cardStyle', 'Simple bordered cards with padding')
        
        # Generate custom CSS based on the analysis
        custom_css = f"""
        /* Typography */
        body {{
            font-family: {body_font};
            font-size: {body_size};
            color: {text_color};
            background-color: {background_color};
            line-height: 1.6;
            margin: 0;
            padding: 0;
        }}
        
        h1, h2, h3, h4, h5, h6 {{
            font-family: {heading_font};
            color: {primary_color};
            margin-bottom: 1rem;
        }}
        
        h1 {{ font-size: {h1_size}; }}
        h2 {{ font-size: {h2_size}; }}
        h3 {{ font-size: {h3_size}; }}
        
        /* Layout */
        .container {{
            max-width: {container_width};
            padding: 0 15px;
            margin: 0 auto;
        }}
        
        /* Header */
        .site-header {{
            background-color: {primary_color};
            color: #fff;
            padding: {spacing} 0;
            margin-bottom: calc({spacing} * 2);
        }}
        
        .site-title {{
            font-size: calc({h1_size} * 1.2);
            font-weight: bold;
            margin: 0;
        }}
        
        .site-navigation {{
            display: flex;
            margin-top: 1rem;
        }}
        
        .site-navigation a {{
            color: #fff;
            margin-right: 1rem;
            text-decoration: none;
            padding: 0.5rem 0;
        }}
        
        .site-navigation a:hover {{
            text-decoration: underline;
        }}
        
        /* Blog Posts */
        .blog-post-card {{
            border: 1px solid #eee;
            border-radius: 8px;
            padding: calc({spacing} * 1.5);
            margin-bottom: calc({spacing} * 1.5);
            background-color: #fff;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        
        .blog-post-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        }}
        
        .blog-post-card h3 {{
            color: {primary_color};
            margin-top: 0;
            margin-bottom: 0.75rem;
        }}
        
        .blog-post-card a {{
            color: {primary_color};
            text-decoration: none;
        }}
        
        .blog-post-card a:hover {{
            text-decoration: underline;
        }}
        
        /* Footer */
        .site-footer {{
            background-color: {secondary_color};
            color: #fff;
            padding: calc({spacing} * 2) 0;
            margin-top: calc({spacing} * 3);
            text-align: center;
        }}
        
        /* Buttons */
        .btn {{
            display: inline-block;
            background-color: {primary_color};
            color: #fff;
            padding: 0.5rem 1.5rem;
            border-radius: 4px;
            text-decoration: none;
            transition: background-color 0.2s;
        }}
        
        .btn:hover {{
            background-color: {accent_color};
        }}
        """
        
        # Create the HTML template with link to external CSS
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{business.get('name', 'Blog')} - Blog</title>
    <meta name="description" content="The official blog for {business.get('name', 'our website')}">
    <link rel="stylesheet" href="https://ourdomain.com/cssstyles/{css_filename}">
    <style>
        {custom_css}
    </style>
</head>
<body>
    <header class="site-header">
        <div class="container">
            <h1 class="site-title">{business.get('name', 'Our')} Blog</h1>
            <nav class="site-navigation">
                <a href="../index.html">Home</a>
                <a href="blog.html">Blog</a>
                <a href="../index.html#contact">Contact</a>
            </nav>
        </div>
    </header>

    <main class="container">
        <section class="blog-posts">
            <h2>Latest Articles</h2>
            
            <!-- BLOG_POSTS_PLACEHOLDER -->
            
        </section>
    </main>

    <footer class="site-footer">
        <div class="container">
            <p>&copy; {datetime.now().year} {business.get('name', 'Website')} - All rights reserved</p>
        </div>
    </footer>
    
    <script src="https://ourdomain.com/scripts/{js_filename if js_filename else ''}"></script>
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
        
        # Extract font families and sizes from typography
        heading_font = typography.get('headingFont', 'sans-serif')
        body_font = typography.get('bodyFont', 'sans-serif')
        h1_size = typography.get('headingSizes', {}).get('h1', '2rem')
        h2_size = typography.get('headingSizes', {}).get('h2', '1.75rem')
        h3_size = typography.get('headingSizes', {}).get('h3', '1.5rem')
        body_size = typography.get('bodySize', '1rem')
        
        # Extract colors
        primary_color = colors.get('primary', '#007bff')
        secondary_color = colors.get('secondary', '#6c757d')
        background_color = colors.get('background', '#ffffff')
        text_color = colors.get('text', '#333333')
        accent_color = colors.get('accent', '#17a2b8')
        
        # Extract layout information
        container_width = layout.get('containerWidth', '1200px')
        spacing = layout.get('spacing', '1rem')
        
        # Generate custom CSS based on the analysis
        custom_css = f"""
        /* Typography */
        body {{
            font-family: {body_font};
            font-size: {body_size};
            color: {text_color};
            background-color: {background_color};
            line-height: 1.6;
            margin: 0;
            padding: 0;
        }}
        
        h1, h2, h3, h4, h5, h6 {{
            font-family: {heading_font};
            color: {primary_color};
            margin-bottom: 1rem;
        }}
        
        h1 {{ font-size: {h1_size}; font-weight: bold; }}
        h2 {{ font-size: {h2_size}; margin-top: 2.5rem; }}
        h3 {{ font-size: {h3_size}; margin-top: 2rem; }}
        
        p {{ margin-bottom: 1.5rem; }}
        
        /* Layout */
        .container {{
            max-width: {container_width};
            padding: 0 15px;
            margin: 0 auto;
        }}
        
        /* Header */
        .site-header {{
            background-color: {primary_color};
            color: #fff;
            padding: {spacing} 0;
            margin-bottom: calc({spacing} * 2);
        }}
        
        .site-title {{
            font-size: calc({h1_size} * 1.2);
            font-weight: bold;
            margin: 0;
        }}
        
        .site-navigation {{
            display: flex;
            margin-top: 1rem;
        }}
        
        .site-navigation a {{
            color: #fff;
            margin-right: 1rem;
            text-decoration: none;
            padding: 0.5rem 0;
        }}
        
        .site-navigation a:hover {{
            text-decoration: underline;
        }}
        
        /* Blog Post */
        .blog-post {{
            background-color: #fff;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
            padding: calc({spacing} * 2);
        }}
        
        .post-header {{
            margin-bottom: calc({spacing} * 2);
        }}
        
        .post-title {{
            color: {primary_color};
            font-size: {h1_size};
            margin-bottom: 0.5rem;
        }}
        
        .post-meta {{
            color: {secondary_color};
            font-size: 0.9rem;
            margin-bottom: 2rem;
        }}
        
        .post-content {{
            margin-bottom: 3rem;
        }}
        
        .post-content img {{
            max-width: 100%;
            height: auto;
            border-radius: 4px;
            margin: 1.5rem 0;
        }}
        
        .post-content ul, .post-content ol {{
            margin-bottom: 1.5rem;
            padding-left: 2rem;
        }}
        
        .post-content blockquote {{
            border-left: 4px solid {primary_color};
            padding-left: 1rem;
            font-style: italic;
            margin: 1.5rem 0;
            color: {secondary_color};
        }}
        
        .post-cta {{
            background-color: #f8f9fa;
            border-radius: 8px;
            padding: calc({spacing} * 1.5);
            margin-top: 3rem;
            text-align: center;
        }}
        
        .post-cta h3 {{
            margin-top: 0;
        }}
        
        /* Footer */
        .site-footer {{
            background-color: {secondary_color};
            color: #fff;
            padding: calc({spacing} * 2) 0;
            margin-top: calc({spacing} * 3);
            text-align: center;
        }}
        
        /* Buttons */
        .btn {{
            display: inline-block;
            background-color: {primary_color};
            color: #fff;
            padding: 0.5rem 1.5rem;
            border-radius: 4px;
            text-decoration: none;
            transition: background-color 0.2s;
        }}
        
        .btn:hover {{
            background-color: {accent_color};
        }}
        
        /* Links */
        a {{
            color: {primary_color};
            text-decoration: none;
            transition: color 0.2s;
        }}
        
        a:hover {{
            color: {accent_color};
        }}
        """
        
        # Create the HTML template with link to external CSS and embedded CSS
        template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{title}} - {business.get('name', 'Blog')}</title>
    <meta name="description" content="{{meta_description}}">
    <link rel="stylesheet" href="https://ourdomain.com/cssstyles/{css_filename}">
    <style>
        {custom_css}
    </style>
</head>
<body>
    <header class="site-header">
        <div class="container">
            <h1 class="site-title">{business.get('name', 'Our')} Blog</h1>
            <nav class="site-navigation">
                <a href="../index.html">Home</a>
                <a href="blog.html">Blog</a>
                <a href="../index.html#contact">Contact</a>
            </nav>
        </div>
    </header>

    <main class="container">
        <article class="blog-post">
            <header class="post-header">
                <h1 class="post-title">{{title}}</h1>
                <div class="post-meta">Published on {{post_date}}</div>
            </header>
            
            <div class="post-content">
                {{content}}
            </div>
            
            <div class="post-cta">
                <h3>Ready to learn more?</h3>
                <p>Check out our website for more information about {business.get('name', 'our services')}.</p>
                <a href="../index.html" class="btn">Visit Website</a>
            </div>
        </article>
    </main>

    <footer class="site-footer">
        <div class="container">
            <p>&copy; {datetime.now().year} {business.get('name', 'Website')} - All rights reserved</p>
        </div>
    </footer>
    
    <script src="https://ourdomain.com/scripts/{js_filename if js_filename else ''}"></script>
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
        # Extract style info if available
        colors = style_analysis.get('colors', {})
        primary_color = colors.get('primary', '#007bff')
        secondary_color = colors.get('secondary', '#6c757d')
        
        # Current date for the post
        current_date = datetime.now().strftime("%Y-%m-%d")
        formatted_date = datetime.now().strftime("%B %d, %Y")
        
        # Format the content for display
        # First handle the content formatting
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
            # Check if it's a list
            elif paragraph.startswith("- ") or paragraph.startswith("* "):
                items = paragraph.split("\n")
                html_content += "<ul>\n"
                for item in items:
                    if item.startswith("- ") or item.startswith("* "):
                        content = item[2:].strip()
                        html_content += f"<li>{content}</li>\n"
                html_content += "</ul>\n"
            # Check if it's a numbered list
            elif re.match(r"^\d+\. ", paragraph):
                items = paragraph.split("\n")
                html_content += "<ol>\n"
                for item in items:
                    if re.match(r"^\d+\. ", item):
                        content = re.sub(r"^\d+\. ", "", item).strip()
                        html_content += f"<li>{content}</li>\n"
                html_content += "</ol>\n"
            # Check for blockquote
            elif paragraph.startswith("> "):
                content = paragraph[2:].strip()
                html_content += f'<blockquote><p>{content}</p></blockquote>\n'
            # Check for code block
            elif paragraph.startswith("```"):
                lines = paragraph.split("\n")
                if len(lines) > 2:
                    code = "\n".join(lines[1:-1]) if lines[-1] == "```" else "\n".join(lines[1:])
                    html_content += f'<pre><code>{code}</code></pre>\n'
                else:
                    html_content += f"<p>{paragraph}</p>\n"
            # Regular paragraph
            else:
                # Look for inline formatting like **bold**, *italic*, and `code`
                paragraph = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", paragraph)
                paragraph = re.sub(r"\*(.*?)\*", r"<em>\1</em>", paragraph)
                paragraph = re.sub(r"`(.*?)`", r"<code>\1</code>", paragraph)
                
                # Convert URLs to links
                paragraph = re.sub(
                    r'(https?://[^\s<>"]+|www\.[^\s<>"]+)',
                    r'<a href="\1" target="_blank">\1</a>',
                    paragraph
                )
                
                html_content += f"<p>{paragraph}</p>\n"
        
        return html_content
        
    except Exception as e:
        logging.error(f"Error formatting blog HTML: {str(e)}")
        return f"<p>{content}</p>"