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
        
        # Determine header class based on header style
        header_class = "blog-header"
        if "navigation" in layout.get('headerStyle', '').lower():
            header_class += " with-navigation"
        
        # Determine button class based on button style
        button_class = "btn"
        if "rounded" in components.get('buttonStyle', '').lower():
            button_class += " btn-rounded"
        elif "square" in components.get('buttonStyle', '').lower():
            button_class += " btn-square"
        
        # Create header based on the analyzed style
        header_style = layout.get('headerStyle', '').lower()
        header_html = f"""
    <header class="{header_class}">
        <div class="container">
            <div class="blog-header-content">
                <h1 class="blog-title">{business.get('name', 'Our')} Blog</h1>
                <nav class="blog-nav">
                    <ul class="nav-list">
                        <li class="nav-item"><a href="../index.html" class="nav-link">Home</a></li>
                        <li class="nav-item"><a href="blog.html" class="nav-link active">Blog</a></li>
                    </ul>
                </nav>
            </div>
        </div>
    </header>"""
        
        # Create blog post card template based on card style
        card_style = components.get('cardStyle', '').lower()
        card_class = "blog-post-card"
        if "shadow" in card_style:
            card_class += " with-shadow"
        if "rounded" in card_style:
            card_class += " rounded"
        if "border" in card_style:
            card_class += " bordered"
            
        # Determine footer style
        footer_style = layout.get('footerStyle', '').lower()
        footer_class = "blog-footer"
        if "comprehensive" in footer_style:
            footer_class += " comprehensive"
        elif "standard" in footer_style:
            footer_class += " standard"
            
        # Combine everything into the template
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{business.get('name', 'Blog')} - Blog</title>
    <meta name="description" content="The official blog for {business.get('name', 'our website')}">
    <link rel="stylesheet" href="assets/css/blog-styles.css">
    <script src="assets/js/blog-scripts.js" defer></script>
    <style>
        /* Inline styles to enhance the connection to the original website */
        :root {{
            --primary-color: {colors.get('primary', '#007bff')};
            --secondary-color: {colors.get('secondary', '#6c757d')};
            --background-color: {colors.get('background', '#ffffff')};
            --text-color: {colors.get('text', '#333333')};
            --accent-color: {colors.get('accent', '#17a2b8')};
            --heading-font: {typography.get('headingFont', 'sans-serif')};
            --body-font: {typography.get('bodyFont', 'sans-serif')};
            --container-width: {layout.get('containerWidth', '1200px')};
            --spacing: {layout.get('spacing', '1rem')};
        }}
        
        body {{
            font-family: var(--body-font);
            color: var(--text-color);
            background-color: var(--background-color);
            line-height: 1.6;
            margin: 0;
            padding: 0;
        }}
        
        h1, h2, h3, h4, h5, h6 {{
            font-family: var(--heading-font);
        }}
        
        h1 {{ font-size: {typography.get('headingSizes', {}).get('h1', '2rem')}; }}
        h2 {{ font-size: {typography.get('headingSizes', {}).get('h2', '1.75rem')}; }}
        h3 {{ font-size: {typography.get('headingSizes', {}).get('h3', '1.5rem')}; }}
        
        p {{ font-size: {typography.get('bodySize', '1rem')}; }}
        
        .container {{
            max-width: var(--container-width);
            margin: 0 auto;
            padding: var(--spacing);
        }}
        
        a {{
            color: var(--primary-color);
            text-decoration: {"none" if "non-underlined" in components.get('linkStyle', '').lower() else "underline"};
        }}
        
        a:hover {{
            color: var(--accent-color);
        }}
        
        .{button_class} {{
            display: inline-block;
            padding: 0.5rem 1rem;
            background-color: var(--primary-color);
            color: #fff;
            text-decoration: none;
            border: none;
            cursor: pointer;
            transition: all 0.3s ease;
        }}
        
        .{button_class}:hover {{
            background-color: var(--accent-color);
        }}
        
        .{card_class} {{
            margin-bottom: 2rem;
            padding: 1.5rem;
            background-color: #fff;
            ${("box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);" if "shadow" in card_class else "")}
            ${("border-radius: 8px;" if "rounded" in card_class else "")}
            ${("border: 1px solid #ddd;" if "bordered" in card_class else "")}
        }}
        
        .blog-title {{
            color: var(--primary-color);
            margin-bottom: 1rem;
        }}
        
        .{footer_class} {{
            background-color: var(--secondary-color);
            color: #fff;
            padding: 2rem 0;
            margin-top: 3rem;
        }}
    </style>
</head>
<body>
{header_html}

    <main class="blog-main">
        <div class="container">
            <section class="blog-posts">
                <h2 class="section-title">Latest Posts</h2>
                
                <!-- BLOG_POSTS_PLACEHOLDER -->
                
            </section>
        </div>
    </main>

    <footer class="{footer_class}">
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
    <link rel="stylesheet" href="assets/css/blog-styles.css">
    <script src="assets/js/blog-scripts.js" defer></script>
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
        
        # Determine header class based on header style
        header_class = "blog-header"
        if "navigation" in layout.get('headerStyle', '').lower():
            header_class += " with-navigation"
        
        # Determine button class based on button style
        button_class = "btn"
        if "rounded" in components.get('buttonStyle', '').lower():
            button_class += " btn-rounded"
        elif "square" in components.get('buttonStyle', '').lower():
            button_class += " btn-square"
        
        # Create header based on the analyzed style
        header_style = layout.get('headerStyle', '').lower()
        header_html = f"""
    <header class="{header_class}">
        <div class="container">
            <div class="blog-header-content">
                <h1 class="blog-title">{business.get('name', 'Our')} Blog</h1>
                <nav class="blog-nav">
                    <ul class="nav-list">
                        <li class="nav-item"><a href="../../index.html" class="nav-link">Home</a></li>
                        <li class="nav-item"><a href="../blog.html" class="nav-link">Blog</a></li>
                    </ul>
                </nav>
            </div>
        </div>
    </header>"""
        
        # Determine footer style
        footer_style = layout.get('footerStyle', '').lower()
        footer_class = "blog-footer"
        if "comprehensive" in footer_style:
            footer_class += " comprehensive"
        elif "standard" in footer_style:
            footer_class += " standard"
            
        # Create the HTML template
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{POST_TITLE}} - {business.get('name', 'Blog')}</title>
    <meta name="description" content="{{POST_META_DESCRIPTION}}">
    <link rel="stylesheet" href="../assets/css/blog-styles.css">
    <script src="../assets/js/blog-scripts.js" defer></script>
    <style>
        /* Inline styles to enhance the connection to the original website */
        :root {{
            --primary-color: {colors.get('primary', '#007bff')};
            --secondary-color: {colors.get('secondary', '#6c757d')};
            --background-color: {colors.get('background', '#ffffff')};
            --text-color: {colors.get('text', '#333333')};
            --accent-color: {colors.get('accent', '#17a2b8')};
            --heading-font: {typography.get('headingFont', 'sans-serif')};
            --body-font: {typography.get('bodyFont', 'sans-serif')};
            --container-width: {layout.get('containerWidth', '1200px')};
            --spacing: {layout.get('spacing', '1rem')};
        }}
        
        body {{
            font-family: var(--body-font);
            color: var(--text-color);
            background-color: var(--background-color);
            line-height: 1.6;
            margin: 0;
            padding: 0;
        }}
        
        h1, h2, h3, h4, h5, h6 {{
            font-family: var(--heading-font);
        }}
        
        h1 {{ font-size: {typography.get('headingSizes', {}).get('h1', '2rem')}; }}
        h2 {{ font-size: {typography.get('headingSizes', {}).get('h2', '1.75rem')}; }}
        h3 {{ font-size: {typography.get('headingSizes', {}).get('h3', '1.5rem')}; }}
        
        p {{ font-size: {typography.get('bodySize', '1rem')}; }}
        
        .container {{
            max-width: var(--container-width);
            margin: 0 auto;
            padding: var(--spacing);
        }}
        
        a {{
            color: var(--primary-color);
            text-decoration: {"none" if "non-underlined" in components.get('linkStyle', '').lower() else "underline"};
        }}
        
        a:hover {{
            color: var(--accent-color);
        }}
        
        .{button_class} {{
            display: inline-block;
            padding: 0.5rem 1rem;
            background-color: var(--primary-color);
            color: #fff;
            text-decoration: none;
            border: none;
            cursor: pointer;
            transition: all 0.3s ease;
            ${("border-radius: 20px;" if "rounded" in button_class else "")}
        }}
        
        .{button_class}:hover {{
            background-color: var(--accent-color);
        }}
        
        .blog-post {{
            padding: 2rem 0;
        }}
        
        .post-header {{
            margin-bottom: 2rem;
        }}
        
        .post-title {{
            color: var(--primary-color);
            margin-bottom: 1rem;
        }}
        
        .post-meta {{
            color: var(--secondary-color);
            font-style: italic;
            margin-bottom: 1rem;
        }}
        
        .post-content {{
            margin-bottom: 3rem;
        }}
        
        .post-content p {{
            margin-bottom: 1.5rem;
        }}
        
        .post-content img {{
            max-width: 100%;
            height: auto;
            margin: 2rem 0;
            ${("border-radius: 8px;" if "rounded" in components.get('cardStyle', '').lower() else "")}
        }}
        
        .post-content h2, .post-content h3 {{
            margin-top: 2rem;
            margin-bottom: 1rem;
            color: var(--primary-color);
        }}
        
        .post-cta {{
            background-color: var(--background-color);
            padding: 2rem;
            margin-top: 3rem;
            border-top: 1px solid var(--secondary-color);
            text-align: center;
        }}
        
        .{footer_class} {{
            background-color: var(--secondary-color);
            color: #fff;
            padding: 2rem 0;
            margin-top: 3rem;
        }}
    </style>
</head>
<body>
{header_html}

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
                    <a href="../../index.html" class="{button_class}">Learn More</a>
                </div>
            </article>
        </div>
    </main>

    <footer class="{footer_class}">
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
    <link rel="stylesheet" href="../assets/css/blog-styles.css">
    <script src="../assets/js/blog-scripts.js" defer></script>
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
