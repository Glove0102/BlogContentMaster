import os
import json
import requests
from openai import OpenAI
import logging
import tempfile
import re
from bs4 import BeautifulSoup
from datetime import datetime

# Initialize OpenAI client
# The newest OpenAI model is "gpt-4o" which was released May 13, 2024.
# Do not change this unless explicitly requested by the user
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
openai = OpenAI(api_key=OPENAI_API_KEY)

def analyze_website_content(html_path, css_path, website_purpose):
    """
    Analyze website content using the OpenAI API to understand:
    - Design patterns
    - Colors
    - Typography
    - Layout
    - Website purpose
    - Business context
    """
    try:
        # Read the HTML and CSS files
        with open(html_path, 'r', encoding='utf-8') as html_file:
            html_content = html_file.read()
        
        with open(css_path, 'r', encoding='utf-8') as css_file:
            css_content = css_file.read()
        
        # Define the JSON structure template outside the f-string
        json_structure = '''
        {
            "colors": {
                "primary": "color value",
                "secondary": "color value",
                "background": "color value",
                "text": "color value",
                "accent": "color value"
            },
            "typography": {
                "headingFont": "font family",
                "bodyFont": "font family",
                "headingSizes": {
                    "h1": "size",
                    "h2": "size",
                    "h3": "size"
                },
                "bodySize": "size"
            },
            "layout": {
                "containerWidth": "width",
                "spacing": "value",
                "headerStyle": "description",
                "footerStyle": "description"
            },
            "components": {
                "buttonStyle": "description",
                "linkStyle": "description",
                "cardStyle": "description"
            },
            "business": {
                "name": "business name",
                "industry": "industry type",
                "audience": "target audience",
                "purpose": "website purpose"
            }
        }
        '''
        
        # Create the prompt with properly formatted content
        prompt = f"""
        I need you to analyze this website's HTML and CSS to understand its design style and purpose.
        
        HTML CONTENT:
        ```html
        {html_content[:15000]}
        ```
        
        CSS CONTENT:
        ```css
        {css_content[:15000]}
        ```
        
        WEBSITE PURPOSE:
        {website_purpose}
        
        Analyze the design style, color scheme, typography, layout, and business context.
        Return a detailed analysis in JSON format with the following structure:
        {json_structure}
        """
        
        # Call OpenAI API
        response = openai.chat.completions.create(
            model="gpt-4.1-nano-2025-04-14",
            messages=[
                {"role": "system", "content": "You are a design analyzer specializing in website style analysis."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        
        # Parse the response
        if response.choices and hasattr(response.choices[0], 'message') and response.choices[0].message and response.choices[0].message.content:
            content = response.choices[0].message.content
            if content:
                analysis_result = json.loads(content)
                return analysis_result
        
        # If we get here, there was a problem with the response
        logging.error("Invalid or empty response from OpenAI API")
        raise ValueError("Invalid or empty response from OpenAI API")
    
    except Exception as e:
        logging.error(f"Error analyzing website content: {str(e)}")
        # Return default analysis if error occurs
        return {
            "colors": {
                "primary": "#007bff",
                "secondary": "#6c757d",
                "background": "#ffffff",
                "text": "#333333",
                "accent": "#17a2b8"
            },
            "typography": {
                "headingFont": "sans-serif",
                "bodyFont": "sans-serif",
                "headingSizes": {
                    "h1": "2rem",
                    "h2": "1.75rem",
                    "h3": "1.5rem"
                },
                "bodySize": "1rem"
            },
            "layout": {
                "containerWidth": "1200px",
                "spacing": "1rem",
                "headerStyle": "Simple header with logo and navigation",
                "footerStyle": "Basic footer with copyright information"
            },
            "components": {
                "buttonStyle": "Standard rounded buttons with hover effect",
                "linkStyle": "Underlined links with color change on hover",
                "cardStyle": "Simple bordered cards with padding"
            },
            "business": {
                "name": "Website",
                "industry": "Technology",
                "audience": "Developers",
                "purpose": website_purpose
            }
        }

def generate_blog_title(topic=None, inspiration_url=None, website_info=None):
    """
    Generate a title for a blog post using OpenAI.
    
    Args:
        topic: Optional topic description
        inspiration_url: Optional URL to scrape for inspiration
        website_info: Information about the website's purpose
        
    Returns:
        A string containing the generated title
    """
    try:
        # Prepare context from topic or inspiration URL
        context = ""
        
        # If we have a topic, use that
        if topic:
            context = f"Topic to write about: {topic}"
        # If we have an inspiration URL, scrape it
        elif inspiration_url:
            try:
                response = requests.get(inspiration_url, timeout=10)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Remove script and style elements
                    for script in soup(["script", "style"]):
                        script.extract()
                    
                    # Get text from the page
                    page_text = soup.get_text()
                    
                    # Clean up text
                    lines = (line.strip() for line in page_text.splitlines())
                    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                    page_text = '\n'.join(chunk for chunk in chunks if chunk)
                    
                    # Trim to a reasonable length
                    context = f"Inspiration URL content: {page_text[:3000]}"
                else:
                    context = f"Unable to fetch content from URL: {inspiration_url}"
            except Exception as e:
                logging.error(f"Error fetching URL: {str(e)}")
                context = f"Unable to fetch content from URL: {inspiration_url}"
        
        # Create a prompt for the OpenAI API
        prompt = f"""
        Generate an engaging, compelling, and SEO-friendly title for a blog post on the following:
        
        CONTEXT INFORMATION:
        {context}
        
        WEBSITE INFORMATION:
        {website_info or "Unknown website"}
        
        The title should be:
        1. Attention-grabbing and engaging
        2. Clear and descriptive of the content
        3. Optimized for search engines
        4. Between 50-70 characters (ideal for SEO)
        5. Relevant to the website's industry and audience
        
        Return only the title text, nothing else.
        """
        
        # Call OpenAI API
        response = openai.chat.completions.create(
            model="gpt-4.1-nano-2025-04-14",
            messages=[
                {"role": "system", "content": "You are a professional blog title generator with expertise in SEO and content marketing."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=50
        )
        
        # Safely get the content from the response
        if response.choices and hasattr(response.choices[0], 'message') and response.choices[0].message and response.choices[0].message.content:
            title = response.choices[0].message.content.strip()
            # Remove any quotes that might be in the response
            title = title.replace('"', '').replace("'", '').strip()
            return title
        
        return "Blog Post" # Fallback title
    
    except Exception as e:
        logging.error(f"Error generating blog title: {str(e)}")
        return "Blog Post"

def generate_blog_content(title, topic=None, content=None, inspiration_url=None, website_info=None, style_analysis=None):
    """
    Generate blog post content using OpenAI.
    
    Args:
        title: The title of the blog post
        topic: Optional topic description
        content: Optional existing content (for editing)
        inspiration_url: Optional URL to scrape for inspiration
        website_info: Information about the website's purpose
        style_analysis: Analysis of the website's style
        
    Returns:
        Dictionary with generated content and metadata
    """
    try:
        # Prepare context from existing content or inspiration URL
        context = ""
        
        # If we have existing content, use that
        if content:
            context = f"Existing content to improve: {content}"
        # If we have a topic, use that
        elif topic:
            context = f"Topic to write about: {topic}"
        # If we have an inspiration URL, scrape it
        elif inspiration_url:
            try:
                response = requests.get(inspiration_url, timeout=10)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Remove script and style elements
                    for script in soup(["script", "style"]):
                        script.extract()
                    
                    # Get text from the page
                    page_text = soup.get_text()
                    
                    # Clean up text
                    lines = (line.strip() for line in page_text.splitlines())
                    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                    page_text = '\n'.join(chunk for chunk in chunks if chunk)
                    
                    # Trim to a reasonable length
                    context = f"Inspiration URL content: {page_text[:5000]}"
                else:
                    context = f"Unable to fetch content from URL. Please write based on the title: {title}"
            except Exception as e:
                logging.error(f"Error fetching URL: {str(e)}")
                context = f"Unable to fetch content from URL. Please write based on the title: {title}"
        
        # Create a prompt for the OpenAI API
        prompt = f"""
        Write a high-quality blog post with the following title:
        
        TITLE: {title}
        
        CONTEXT INFORMATION:
        {context}
        
        WEBSITE INFORMATION:
        {website_info or "Unknown website"}
        
        Please follow these guidelines:
        1. Write in a professional but engaging tone
        2. Include contextual references to the website/product
        3. Incorporate a call-to-action that directs readers to the main website
        4. Structure with clear headings, paragraphs, and bullet points where appropriate
        5. Make it SEO-friendly
        6. Keep the content factually accurate
        7. Aim for approximately 800-1000 words
        
        The blog post should feel like a natural part of the website.
        """
        
        # Call OpenAI API
        response = openai.chat.completions.create(
            model="gpt-4.1-nano-2025-04-14",
            messages=[
                {"role": "system", "content": "You are a professional blog content writer specializing in creating content that matches a website's style and purpose."},
                {"role": "user", "content": prompt}
            ]
        )
        
        # Safely get the content from the response
        blog_content = "Failed to generate content"
        if response.choices and hasattr(response.choices[0], 'message') and response.choices[0].message and response.choices[0].message.content:
            blog_content = response.choices[0].message.content
        
        # Generate a comprehensive meta description
        meta_description_prompt = f"""
        Generate an SEO-friendly meta description for this blog post.
        
        BLOG TITLE: '{title}'
        
        BLOG CONTENT SUMMARY:
        {blog_content[:500]}
        
        Requirements:
        1. Must be EXACTLY 150-160 characters (maximize character usage within this range)
        2. Include relevant keywords from the title and content
        3. Be compelling and promote click-through
        4. Accurately summarize the content's value proposition
        5. Include a call-to-action if possible
        
        Return ONLY the meta description text. No quotes, no explanations.
        """
        
        meta_response = openai.chat.completions.create(
            model="gpt-4.1-nano-2025-04-14",
            messages=[
                {"role": "system", "content": "You are an SEO specialist creating meta descriptions. You must generate descriptions that use between 150-160 characters."},
                {"role": "user", "content": meta_description_prompt}
            ],
            max_tokens=100
        )
        
        # Safely get the meta description
        meta_description = f"Blog post about {title}"
        if meta_response.choices and hasattr(meta_response.choices[0], 'message') and meta_response.choices[0].message and meta_response.choices[0].message.content:
            content = meta_response.choices[0].message.content
            if content:
                meta_description = content.strip()
                
        # Ensure the meta description doesn't exceed 160 characters
        if len(meta_description) > 160:
            meta_description = meta_description[:157] + '...'
        
        # Format HTML content based on the post template
        formatted_html = format_blog_html(title, blog_content, style_analysis)
        
        return {
            "content": blog_content,
            "meta_description": meta_description,
            "formatted_html": formatted_html
        }
    
    except Exception as e:
        logging.error(f"Error generating blog content: {str(e)}")
        return {
            "content": f"Failed to generate content for '{title}'. Please try again later.",
            "meta_description": f"Blog post about {title}",
            "formatted_html": f"<h1>{title}</h1><p>Failed to generate content. Please try again later.</p>"
        }

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
        # Current date for the post
        current_date = datetime.now().strftime("%Y-%m-%d")
        formatted_date = datetime.now().strftime("%B %d, %Y")
        
        # Process the content to add HTML formatting
        # Convert markdown-style headers to HTML
        content = re.sub(r'^# (.+)$', r'<h1>\1</h1>', content, flags=re.MULTILINE)
        content = re.sub(r'^## (.+)$', r'<h2>\1</h2>', content, flags=re.MULTILINE)
        content = re.sub(r'^### (.+)$', r'<h3>\1</h3>', content, flags=re.MULTILINE)
        
        # Convert markdown-style lists to HTML
        content = re.sub(r'^\* (.+)$', r'<li>\1</li>', content, flags=re.MULTILINE)
        content = re.sub(r'^\d+\. (.+)$', r'<li>\1</li>', content, flags=re.MULTILINE)
        
        # Wrap consecutive list items in ul/ol tags
        content = re.sub(r'(<li>.+</li>\n)+', r'<ul>\n\g<0></ul>\n', content)
        
        # Convert paragraphs (lines with content) to HTML
        content = re.sub(r'^([^<\n].+)$', r'<p>\1</p>', content, flags=re.MULTILINE)
        
        # Clean up any double paragraph tags
        content = re.sub(r'<p><p>', r'<p>', content)
        content = re.sub(r'</p></p>', r'</p>', content)
        
        # Create the formatted HTML
        html = f"""
        <article class="blog-post">
            <header class="post-header">
                <h1 class="post-title">{title}</h1>
                <div class="post-meta">
                    <time datetime="{current_date}">{formatted_date}</time>
                </div>
            </header>
            
            <div class="post-content">
                {content}
            </div>
            
            <div class="post-cta">
                <h3>Ready to get started?</h3>
                <p>Learn more about our services and how we can help you.</p>
                <a href="../../index.html" class="btn btn-primary">Learn More</a>
            </div>
        </article>
        """
        
        return html
    
    except Exception as e:
        logging.error(f"Error formatting blog HTML: {str(e)}")
        return f"<h1>{title}</h1><p>{content}</p>"