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
        
        # Check if it's Battle Stonks or similar
        business_name = business.get('name', '').lower()
        is_gaming_site = 'battle' in business_name or 'stonk' in business_name or 'game' in business_name
        
        # For gaming sites like Battle Stonks, create a dark gaming theme
        if is_gaming_site:
            template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Battle Stonks Blog</title>
    <meta name="description" content="The official blog for Battle Stonks">
    <link rel="stylesheet" href="assets/css/blog-styles.css">
    <script src="assets/js/blog-scripts.js" defer></script>
    <style>
        :root {
            --primary-color: #4ae3ff;
            --secondary-color: #8b55ff;
            --background-color: #111827;
            --text-color: #ffffff;
            --accent-color: #ff3bde;
            --card-bg-color: #1e293b;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Inter', 'Segoe UI', Roboto, sans-serif;
            color: var(--text-color);
            background-color: var(--background-color);
            line-height: 1.6;
        }
        
        h1, h2, h3, h4, h5, h6 {
            font-family: 'Inter', 'Segoe UI', Roboto, sans-serif;
            font-weight: 700;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 2rem;
        }
        
        a {
            color: var(--primary-color);
            text-decoration: none;
            transition: color 0.3s ease;
        }
        
        a:hover {
            color: var(--accent-color);
        }
        
        /* Ticker */
        .ticker {
            background-color: #000;
            color: white;
            padding: 0.5rem 0;
            overflow: hidden;
            white-space: nowrap;
            border-bottom: 1px solid #333;
        }
        
        .ticker-content {
            display: inline-block;
            animation: ticker 35s linear infinite;
        }
        
        .ticker-item {
            display: inline-block;
            margin-right: 2rem;
        }
        
        .ticker-item.positive {
            color: #22c55e;
        }
        
        .ticker-item.negative {
            color: #ef4444;
        }
        
        @keyframes ticker {
            0% { transform: translateX(100%); }
            100% { transform: translateX(-100%); }
        }
        
        /* Header */
        .blog-header {
            padding: 1.5rem 0;
            background-color: var(--background-color);
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .blog-title {
            font-size: 2.5rem;
            color: var(--primary-color);
            text-shadow: 0 0 15px rgba(74, 227, 255, 0.5);
            margin-bottom: 0.5rem;
        }
        
        /* Navigation */
        .blog-nav {
            margin-top: 1rem;
        }
        
        .nav-list {
            list-style: none;
            display: flex;
            gap: 2rem;
            padding: 0;
        }
        
        .nav-item {
            font-size: 1.1rem;
        }
        
        .nav-link {
            color: var(--text-color);
            text-decoration: none;
            padding: 0.5rem 0;
            position: relative;
        }
        
        .nav-link:after {
            content: '';
            position: absolute;
            width: 0;
            height: 2px;
            bottom: 0;
            left: 0;
            background-color: var(--primary-color);
            transition: width 0.3s ease;
        }
        
        .nav-link:hover:after,
        .nav-link.active:after {
            width: 100%;
        }
        
        /* Main Content */
        .blog-main {
            padding: 3rem 0;
        }
        
        .section-title {
            color: var(--text-color);
            margin-bottom: 2rem;
            font-size: 2rem;
            position: relative;
            display: inline-block;
        }
        
        .section-title:after {
            content: '';
            position: absolute;
            bottom: -10px;
            left: 0;
            width: 60px;
            height: 3px;
            background-color: var(--primary-color);
        }
        
        /* Blog Posts */
        .blog-post-card {
            background-color: var(--card-bg-color);
            border-radius: 12px;
            margin-bottom: 1.5rem;
            padding: 1.5rem;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            border-left: 4px solid var(--primary-color);
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
        }
        
        .blog-post-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5);
        }
        
        .blog-post-card h3 {
            margin-bottom: 0.5rem;
        }
        
        .blog-post-card a {
            font-weight: 600;
        }
        
        /* Button Styles */
        .btn {
            display: inline-block;
            padding: 0.75rem 1.5rem;
            background-color: var(--primary-color);
            color: #111827;
            text-decoration: none;
            border: none;
            border-radius: 8px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 0 10px rgba(74, 227, 255, 0.3);
        }
        
        .btn:hover {
            background-color: var(--accent-color);
            box-shadow: 0 0 15px rgba(255, 59, 222, 0.5);
            transform: translateY(-2px);
        }
        
        /* Footer */
        .blog-footer {
            background-color: var(--background-color);
            padding: 2rem 0;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            text-align: center;
            font-size: 0.9rem;
            color: rgba(255, 255, 255, 0.7);
        }
    </style>
</head>
<body>
    <div class="ticker">
        <div class="ticker-content">
            <span class="ticker-item negative">SEMI $679.19 -1.93%</span>
            <span class="ticker-item positive">CLOUD $333.51 +2.63%</span>
            <span class="ticker-item positive">CYBER $212.65 +0.74%</span>
            <span class="ticker-item positive">ENRG $76.00 +0.77%</span>
            <span class="ticker-item negative">SOLAR $48.40 -2.78%</span>
        </div>
    </div>

    <header class="blog-header">
        <div class="container">
            <h1 class="blog-title">Battle Stonks Blog</h1>
            <nav class="blog-nav">
                <ul class="nav-list">
                    <li class="nav-item"><a href="../index.html" class="nav-link">Home</a></li>
                    <li class="nav-item"><a href="blog.html" class="nav-link active">Blog</a></li>
                </ul>
            </nav>
        </div>
    </header>

    <main class="blog-main">
        <div class="container">
            <section class="blog-posts">
                <h2 class="section-title">Latest Posts</h2>
                
                <!-- BLOG_POSTS_PLACEHOLDER -->
                
            </section>
        </div>
    </main>

    <footer class="blog-footer">
        <div class="container">
            <p>&copy; Battle Stonks - All rights reserved</p>
        </div>
    </footer>
</body>
</html>"""
            return template
        
        # For regular websites (non-gaming), use a standard light theme
        else:
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
    <link rel="stylesheet" href="assets/css/blog-styles.css">
    <script src="assets/js/blog-scripts.js" defer></script>
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
        
        h1, h2, h3, h4, h5, h6 {{
            font-family: 'Arial', sans-serif;
        }}
        
        .container {{
            width: 90%;
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 15px;
        }}
        
        a {{
            color: var(--primary-color);
            text-decoration: none;
        }}
        
        a:hover {{
            color: var(--accent-color);
        }}
        
        .blog-header {{
            padding: 1rem 0;
            border-bottom: 1px solid #eee;
        }}
        
        .blog-title {{
            color: var(--primary-color);
        }}
        
        .blog-nav ul {{
            list-style: none;
            padding: 0;
            display: flex;
            gap: 1rem;
        }}
        
        .blog-post-card {{
            margin-bottom: 1.5rem;
            padding-bottom: 1.5rem;
            border-bottom: 1px solid #eee;
        }}
    </style>
</head>
<body>
    <header class="blog-header">
        <div class="container">
            <h1 class="blog-title">{business.get('name', 'Our')} Blog</h1>
            <nav class="blog-nav">
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
            <p>&copy; {business.get('name', 'Website')} - All rights reserved</p>
        </div>
    </footer>
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
    <link rel="stylesheet" href="assets/css/blog-styles.css">
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

def generate_post_template(analysis_result, title, content, meta_description=None):
    """Generate a blog post template based on website analysis"""
    try:
        # Extract style information
        colors = analysis_result.get('colors', {})
        typography = analysis_result.get('typography', {})
        layout = analysis_result.get('layout', {})
        components = analysis_result.get('components', {})
        business = analysis_result.get('business', {})
        
        # Check if it's Battle Stonks or similar
        business_name = business.get('name', '').lower()
        is_gaming_site = 'battle' in business_name or 'stonk' in business_name or 'game' in business_name
        
        # Format the post date
        post_date = datetime.now().strftime("%B %d, %Y")
        
        # For gaming sites like Battle Stonks, create a dark gaming theme
        if is_gaming_site:
            template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Battle Stonks Blog</title>
    <meta name="description" content="{meta_description or 'Read our latest blog post'}">
    <link rel="stylesheet" href="assets/css/blog-styles.css">
    <script src="assets/js/blog-scripts.js" defer></script>
    <style>
        :root {
            --primary-color: #4ae3ff;
            --secondary-color: #8b55ff;
            --background-color: #111827;
            --text-color: #ffffff;
            --accent-color: #ff3bde;
            --card-bg-color: #1e293b;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Inter', 'Segoe UI', Roboto, sans-serif;
            color: var(--text-color);
            background-color: var(--background-color);
            line-height: 1.6;
        }
        
        h1, h2, h3, h4, h5, h6 {
            font-family: 'Inter', 'Segoe UI', Roboto, sans-serif;
            font-weight: 700;
            margin-bottom: 1rem;
        }
        
        p {
            margin-bottom: 1.5rem;
        }
        
        .container {
            max-width: 1000px;
            margin: 0 auto;
            padding: 0 2rem;
        }
        
        a {
            color: var(--primary-color);
            text-decoration: none;
            transition: color 0.3s ease;
        }
        
        a:hover {
            color: var(--accent-color);
        }
        
        /* Ticker */
        .ticker {
            background-color: #000;
            color: white;
            padding: 0.5rem 0;
            overflow: hidden;
            white-space: nowrap;
            border-bottom: 1px solid #333;
        }
        
        .ticker-content {
            display: inline-block;
            animation: ticker 35s linear infinite;
        }
        
        .ticker-item {
            display: inline-block;
            margin-right: 2rem;
        }
        
        .ticker-item.positive {
            color: #22c55e;
        }
        
        .ticker-item.negative {
            color: #ef4444;
        }
        
        @keyframes ticker {
            0% { transform: translateX(100%); }
            100% { transform: translateX(-100%); }
        }
        
        /* Header */
        .blog-header {
            padding: 1.5rem 0;
            background-color: var(--background-color);
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .blog-title {
            font-size: 2.5rem;
            color: var(--primary-color);
            text-shadow: 0 0 15px rgba(74, 227, 255, 0.5);
            margin-bottom: 0.5rem;
        }
        
        /* Navigation */
        .blog-nav {
            margin-top: 1rem;
        }
        
        .nav-list {
            list-style: none;
            display: flex;
            gap: 2rem;
            padding: 0;
        }
        
        .nav-item {
            font-size: 1.1rem;
        }
        
        .nav-link {
            color: var(--text-color);
            text-decoration: none;
            padding: 0.5rem 0;
            position: relative;
        }
        
        .nav-link:after {
            content: '';
            position: absolute;
            width: 0;
            height: 2px;
            bottom: 0;
            left: 0;
            background-color: var(--primary-color);
            transition: width 0.3s ease;
        }
        
        .nav-link:hover:after,
        .nav-link.active:after {
            width: 100%;
        }
        
        /* Post Content */
        .post-header {
            margin: 3rem 0 2rem;
        }
        
        .post-title {
            font-size: 2.8rem;
            color: var(--primary-color);
            margin-bottom: 0.5rem;
            text-shadow: 0 0 10px rgba(74, 227, 255, 0.3);
        }
        
        .post-meta {
            color: rgba(255, 255, 255, 0.7);
            font-size: 0.9rem;
            margin-bottom: 2rem;
        }
        
        .post-content {
            background-color: var(--card-bg-color);
            padding: 2rem;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
            border-left: 4px solid var(--primary-color);
            margin-bottom: 3rem;
        }
        
        .post-content img {
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            margin: 1.5rem 0;
        }
        
        .post-content blockquote {
            border-left: 3px solid var(--accent-color);
            padding-left: 1rem;
            margin: 1.5rem 0;
            font-style: italic;
            color: rgba(255, 255, 255, 0.8);
        }
        
        /* Button Styles */
        .btn {
            display: inline-block;
            padding: 0.75rem 1.5rem;
            background-color: var(--primary-color);
            color: var(--background-color);
            text-decoration: none;
            border: none;
            border-radius: 8px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 0 10px rgba(74, 227, 255, 0.3);
        }
        
        .btn:hover {
            background-color: var(--accent-color);
            box-shadow: 0 0 15px rgba(255, 59, 222, 0.5);
            transform: translateY(-2px);
        }
        
        /* Footer */
        .blog-footer {
            background-color: var(--background-color);
            padding: 2rem 0;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            text-align: center;
            font-size: 0.9rem;
            color: rgba(255, 255, 255, 0.7);
        }
    </style>
</head>
<body>
    <div class="ticker">
        <div class="ticker-content">
            <span class="ticker-item negative">SEMI $679.19 -1.93%</span>
            <span class="ticker-item positive">CLOUD $333.51 +2.63%</span>
            <span class="ticker-item positive">CYBER $212.65 +0.74%</span>
            <span class="ticker-item positive">ENRG $76.00 +0.77%</span>
            <span class="ticker-item negative">SOLAR $48.40 -2.78%</span>
        </div>
    </div>

    <header class="blog-header">
        <div class="container">
            <h1 class="blog-title">Battle Stonks Blog</h1>
            <nav class="blog-nav">
                <ul class="nav-list">
                    <li class="nav-item"><a href="../index.html" class="nav-link">Home</a></li>
                    <li class="nav-item"><a href="blog.html" class="nav-link">Blog</a></li>
                    <li class="nav-item"><a href="#" class="nav-link active">Post</a></li>
                </ul>
            </nav>
        </div>
    </header>

    <main>
        <div class="container">
            <article class="post">
                <header class="post-header">
                    <h1 class="post-title">{title}</h1>
                    <div class="post-meta">Published on {post_date}</div>
                </header>
                <div class="post-content">
                    {content}
                </div>
                <div class="post-navigation">
                    <a href="blog.html" class="btn">← Back to Blog</a>
                </div>
            </article>
        </div>
    </main>

    <footer class="blog-footer">
        <div class="container">
            <p>&copy; Battle Stonks - All rights reserved</p>
        </div>
    </footer>
</body>
</html>"""
            return template
        
        # For regular (non-gaming) websites
        else:
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
    <title>{title} - {business.get('name', 'Blog')}</title>
    <meta name="description" content="{meta_description or 'Read our latest blog post'}">
    <link rel="stylesheet" href="assets/css/blog-styles.css">
    <script src="assets/js/blog-scripts.js" defer></script>
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
        
        h1, h2, h3, h4, h5, h6 {{
            font-family: 'Arial', sans-serif;
            margin-bottom: 1rem;
        }}
        
        p {{
            margin-bottom: 1.5rem;
        }}
        
        .container {{
            width: 90%;
            max-width: 900px;
            margin: 0 auto;
            padding: 0 15px;
        }}
        
        a {{
            color: var(--primary-color);
            text-decoration: none;
        }}
        
        a:hover {{
            color: var(--accent-color);
        }}
        
        .blog-header {{
            padding: 1rem 0;
            border-bottom: 1px solid #eee;
        }}
        
        .blog-title {{
            color: var(--primary-color);
        }}
        
        .blog-nav ul {{
            list-style: none;
            padding: 0;
            display: flex;
            gap: 1rem;
        }}
        
        .post-header {{
            margin: 2rem 0;
        }}
        
        .post-title {{
            color: var(--primary-color);
        }}
        
        .post-meta {{
            color: #666;
            font-size: 0.9rem;
            margin-bottom: 2rem;
        }}
        
        .post-content {{
            margin-bottom: 2rem;
        }}
        
        .post-navigation {{
            margin: 2rem 0;
        }}
    </style>
</head>
<body>
    <header class="blog-header">
        <div class="container">
            <h1 class="blog-title">{business.get('name', 'Our')} Blog</h1>
            <nav class="blog-nav">
                <ul>
                    <li><a href="../index.html">Home</a></li>
                    <li><a href="blog.html">Blog</a></li>
                </ul>
            </nav>
        </div>
    </header>

    <main>
        <div class="container">
            <article class="post">
                <header class="post-header">
                    <h1 class="post-title">{title}</h1>
                    <div class="post-meta">Published on {post_date}</div>
                </header>
                <div class="post-content">
                    {content}
                </div>
                <div class="post-navigation">
                    <a href="blog.html">← Back to Blog</a>
                </div>
            </article>
        </div>
    </main>

    <footer>
        <div class="container">
            <p>&copy; {business.get('name', 'Website')} - All rights reserved</p>
        </div>
    </footer>
</body>
</html>"""
            return html
    
    except Exception as e:
        logging.error(f"Error generating post template: {str(e)}")
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link rel="stylesheet" href="assets/css/blog-styles.css">
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
            <article>
                <h1>{title}</h1>
                <div>
                    {content}
                </div>
                <div>
                    <a href="blog.html">Back to Blog</a>
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
        
        .nav-link {
            color: var(--text-color);
            text-decoration: none;
            padding: 0.5rem 0;
            position: relative;
        }
        
        .nav-link:after {
            content: '';
            position: absolute;
            width: 0;
            height: 2px;
            bottom: 0;
            left: 0;
            background-color: var(--primary-color);
            transition: width 0.3s ease;
        }
        
        .nav-link:hover:after,
        .nav-link.active:after {
            width: 100%;
        }
        
        /* Main Content */
        .blog-main {
            padding: 3rem 0;
        }
        
        .section-title {
            color: var(--text-color);
            margin-bottom: 2rem;
            font-size: 2rem;
            position: relative;
            display: inline-block;
        }
        
        .section-title:after {
            content: '';
            position: absolute;
            bottom: -10px;
            left: 0;
            width: 60px;
            height: 3px;
            background-color: var(--primary-color);
        }
        
        /* Blog Posts */
        .blog-post-card {
            background-color: var(--card-bg-color);
            border-radius: 12px;
            margin-bottom: 1.5rem;
            padding: 1.5rem;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            border-left: 4px solid var(--primary-color);
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
        }
        
        .blog-post-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5);
        }
        
        .blog-post-card h3 {
            margin-bottom: 0.5rem;
        }
        
        .blog-post-card a {
            font-weight: 600;
        }
        
        /* Button Styles */
        .btn {
            display: inline-block;
            padding: 0.75rem 1.5rem;
            background-color: var(--primary-color);
            color: var(--background-color);
            text-decoration: none;
            border: none;
            border-radius: 8px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 0 10px rgba(74, 227, 255, 0.3);
        }
        
        .btn:hover {
            background-color: var(--accent-color);
            box-shadow: 0 0 15px rgba(255, 59, 222, 0.5);
            transform: translateY(-2px);
        }
        
        /* Footer */
        .blog-footer {
            background-color: var(--nav-bg-color);
            padding: 2rem 0;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            text-align: center;
            font-size: 0.9rem;
            color: rgba(255, 255, 255, 0.7);
        }
    </style>
</head>
<body>
    <div class="ticker">
        <div class="ticker-content">
            <span class="ticker-item negative">SEMI $679.19 -1.93%</span>
            <span class="ticker-item positive">CLOUD $333.51 +2.63%</span>
            <span class="ticker-item positive">CYBER $212.65 +0.74%</span>
            <span class="ticker-item positive">ENRG $76.00 +0.77%</span>
            <span class="ticker-item negative">SOLAR $48.40 -2.78%</span>
            <span class="ticker-item negative">SEMI $679.19 -1.93%</span>
            <span class="ticker-item positive">CLOUD $333.51 +2.63%</span>
            <span class="ticker-item positive">CYBER $212.65 +0.74%</span>
            <span class="ticker-item positive">ENRG $76.00 +0.77%</span>
            <span class="ticker-item negative">SOLAR $48.40 -2.78%</span>
        </div>
    </div>

    <header class="blog-header">
        <div class="container">
            <h1 class="blog-title">Battle Stonks Blog</h1>
            <nav class="blog-nav">
                <ul class="nav-list">
                    <li class="nav-item"><a href="../index.html" class="nav-link">Home</a></li>
                    <li class="nav-item"><a href="blog.html" class="nav-link active">Blog</a></li>
                </ul>
            </nav>
        </div>
    </header>

    <main class="blog-main">
        <div class="container">
            <section class="blog-posts">
                <h2 class="section-title">Latest Posts</h2>
                
                <!-- BLOG_POSTS_PLACEHOLDER -->
                
            </section>
        </div>
    </main>

    <footer class="blog-footer">
        <div class="container">
            <p>&copy; Battle Stonks - All rights reserved</p>
        </div>
    </footer>
</body>
</html>"""
            
        # Normal template for other websites
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
