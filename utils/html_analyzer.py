import os
import re
import json
import logging
from bs4 import BeautifulSoup
import tinycss2
from collections import Counter

def analyze_html_css(html_path, css_path):
    """
    Analyze HTML and CSS files to extract design patterns, colors, typography, and layout information.
    """
    try:
        # Read the HTML file
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Read the CSS file
        with open(css_path, 'r', encoding='utf-8') as f:
            css_content = f.read()
        
        # Parse HTML with BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Extract colors from CSS
        colors = extract_colors(css_content)
        
        # Extract typography from CSS
        typography = extract_typography(css_content)
        
        # Extract layout information
        layout = extract_layout(soup, css_content)
        
        # Extract component styles
        components = extract_components(soup, css_content)
        
        # Return the analysis results
        return {
            "colors": colors,
            "typography": typography,
            "layout": layout,
            "components": components
        }
    
    except Exception as e:
        logging.error(f"Error analyzing HTML/CSS: {str(e)}")
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
            }
        }

def extract_colors(css_content):
    """Extract color values from CSS content."""
    # Find all color values in the CSS with their selector context
    color_pattern = r'([^{]*){[^}]*(?:color|background|background-color|border-color|fill|stroke)\s*:\s*(#[0-9a-fA-F]{3,8}|rgba?\([^)]+\)|hsla?\([^)]+\)|[a-zA-Z]+)[^}]*}'
    context_color_matches = re.findall(color_pattern, css_content)
    
    # Extract just the colors for frequency counting
    color_matches = []
    for _, props in context_color_matches:
        colors = re.findall(r'(?:color|background|background-color|border-color|fill|stroke)\s*:\s*(#[0-9a-fA-F]{3,8}|rgba?\([^)]+\)|hsla?\([^)]+\)|[a-zA-Z]+)', props)
        color_matches.extend(colors)
    
    # Count occurrences of each color
    color_counter = Counter(color_matches)
    most_common_colors = color_counter.most_common(15)  # Increased from 10 to 15
    
    # Assign roles to colors based on their frequency and context
    primary_color = most_common_colors[0][0] if most_common_colors else "#007bff"
    secondary_color = most_common_colors[1][0] if len(most_common_colors) > 1 else "#6c757d"
    background_color = "#ffffff"  # Default
    text_color = "#333333"  # Default
    accent_color = most_common_colors[2][0] if len(most_common_colors) > 2 else "#17a2b8"
    
    # Try to identify background and text colors
    bg_pattern = r'(?:body|html|:root|\.main|\.container|main|#main)\s*{[^}]*background(?:-color)?\s*:\s*([^;]+)'
    bg_match = re.search(bg_pattern, css_content)
    if bg_match:
        background_color = bg_match.group(1).strip()
    
    text_pattern = r'(?:body|html|:root|\.main|\.container|main|#main)\s*{[^}]*color\s*:\s*([^;]+)'
    text_match = re.search(text_pattern, css_content)
    if text_match:
        text_color = text_match.group(1).strip()
    
    # Look for button colors
    button_color = None
    button_pattern = r'(?:\.btn|button|\.button|input\[type="submit"\])\s*{[^}]*background(?:-color)?\s*:\s*([^;]+)'
    button_match = re.search(button_pattern, css_content)
    if button_match:
        button_color = button_match.group(1).strip()
    
    # Look for link colors
    link_color = None
    link_pattern = r'a\s*{[^}]*color\s*:\s*([^;]+)'
    link_match = re.search(link_pattern, css_content)
    if link_match:
        link_color = link_match.group(1).strip()
    
    # Look for heading colors
    heading_color = None
    heading_pattern = r'(?:h1|h2|h3|\.heading)\s*{[^}]*color\s*:\s*([^;]+)'
    heading_match = re.search(heading_pattern, css_content)
    if heading_match:
        heading_color = heading_match.group(1).strip()
    
    # Look for border colors
    border_color = None
    border_pattern = r'{[^}]*border(?:-color)?\s*:\s*([^;]+)}'
    border_matches = re.findall(border_pattern, css_content)
    if border_matches:
        # Try to extract just the color part from border properties
        for border in border_matches:
            color_match = re.search(r'(#[0-9a-fA-F]{3,8}|rgba?\([^)]+\)|hsla?\([^)]+\)|[a-zA-Z]+)', border)
            if color_match:
                border_color = color_match.group(1)
                break
    
    # Build a color palette from all the identified colors
    color_palette = [color for color, _ in most_common_colors]
    
    return {
        "primary": primary_color,
        "secondary": secondary_color,
        "background": background_color,
        "text": text_color,
        "accent": accent_color,
        "button": button_color or primary_color,
        "link": link_color or primary_color,
        "heading": heading_color or primary_color,
        "border": border_color or "#dee2e6",
        "palette": color_palette
    }

def extract_typography(css_content):
    """Extract typography information from CSS content."""
    # Default values
    heading_font = "sans-serif"
    body_font = "sans-serif"
    h1_size = "2rem"
    h2_size = "1.75rem"
    h3_size = "1.5rem"
    body_size = "1rem"
    
    # Font weights
    heading_weight = "bold"
    body_weight = "normal"
    
    # Line heights
    heading_line_height = "1.2"
    body_line_height = "1.6"
    
    # Font styles
    heading_style = "normal"
    body_style = "normal"
    
    # Try to find font-family for headings
    heading_font_pattern = r'(?:h1|h2|h3|h4|h5|\.heading)\s*{[^}]*font-family\s*:\s*([^;]+)'
    heading_font_match = re.search(heading_font_pattern, css_content)
    if heading_font_match:
        heading_font = heading_font_match.group(1).strip().strip("'\"")
    
    # Try to find font-family for body
    body_font_pattern = r'(?:body|html|p|:root)\s*{[^}]*font-family\s*:\s*([^;]+)'
    body_font_match = re.search(body_font_pattern, css_content)
    if body_font_match:
        body_font = body_font_match.group(1).strip().strip("'\"")
    
    # Try to find font sizes
    h1_size_pattern = r'h1\s*{[^}]*font-size\s*:\s*([^;]+)'
    h1_match = re.search(h1_size_pattern, css_content)
    if h1_match and h1_match.group(1):
        h1_size = h1_match.group(1).strip()
    
    h2_size_pattern = r'h2\s*{[^}]*font-size\s*:\s*([^;]+)'
    h2_match = re.search(h2_size_pattern, css_content)
    if h2_match and h2_match.group(1):
        h2_size = h2_match.group(1).strip()
    
    h3_size_pattern = r'h3\s*{[^}]*font-size\s*:\s*([^;]+)'
    h3_match = re.search(h3_size_pattern, css_content)
    if h3_match and h3_match.group(1):
        h3_size = h3_match.group(1).strip()
    
    body_size_pattern = r'(?:body|html|p)\s*{[^}]*font-size\s*:\s*([^;]+)'
    body_match = re.search(body_size_pattern, css_content)
    if body_match and body_match.group(1):
        body_size = body_match.group(1).strip()
    
    # Try to find font weights
    heading_weight_pattern = r'(?:h1|h2|h3|\.heading)\s*{[^}]*font-weight\s*:\s*([^;]+)'
    heading_weight_match = re.search(heading_weight_pattern, css_content)
    if heading_weight_match and heading_weight_match.group(1):
        heading_weight = heading_weight_match.group(1).strip()
    
    body_weight_pattern = r'(?:body|html|p)\s*{[^}]*font-weight\s*:\s*([^;]+)'
    body_weight_match = re.search(body_weight_pattern, css_content)
    if body_weight_match and body_weight_match.group(1):
        body_weight = body_weight_match.group(1).strip()
    
    # Try to find line heights
    heading_line_height_pattern = r'(?:h1|h2|h3|\.heading)\s*{[^}]*line-height\s*:\s*([^;]+)'
    heading_line_height_match = re.search(heading_line_height_pattern, css_content)
    if heading_line_height_match and heading_line_height_match.group(1):
        heading_line_height = heading_line_height_match.group(1).strip()
    
    body_line_height_pattern = r'(?:body|html|p)\s*{[^}]*line-height\s*:\s*([^;]+)'
    body_line_height_match = re.search(body_line_height_pattern, css_content)
    if body_line_height_match and body_line_height_match.group(1):
        body_line_height = body_line_height_match.group(1).strip()
    
    # Try to find font styles
    heading_style_pattern = r'(?:h1|h2|h3|\.heading)\s*{[^}]*font-style\s*:\s*([^;]+)'
    heading_style_match = re.search(heading_style_pattern, css_content)
    if heading_style_match and heading_style_match.group(1):
        heading_style = heading_style_match.group(1).strip()
    
    body_style_pattern = r'(?:body|html|p)\s*{[^}]*font-style\s*:\s*([^;]+)'
    body_style_match = re.search(body_style_pattern, css_content)
    if body_style_match and body_style_match.group(1):
        body_style = body_style_match.group(1).strip()
    
    # Try to find paragraph spacing and margins
    paragraph_spacing = "1rem"
    p_margin_pattern = r'p\s*{[^}]*margin-bottom\s*:\s*([^;]+)'
    p_margin_match = re.search(p_margin_pattern, css_content)
    if p_margin_match and p_margin_match.group(1):
        paragraph_spacing = p_margin_match.group(1).strip()
    
    return {
        "headingFont": heading_font,
        "bodyFont": body_font,
        "headingSizes": {
            "h1": h1_size,
            "h2": h2_size,
            "h3": h3_size
        },
        "bodySize": body_size,
        "headingWeight": heading_weight,
        "bodyWeight": body_weight,
        "headingLineHeight": heading_line_height,
        "bodyLineHeight": body_line_height,
        "headingStyle": heading_style,
        "bodyStyle": body_style,
        "paragraphSpacing": paragraph_spacing
    }

def extract_layout(soup, css_content):
    """Extract layout information from HTML and CSS."""
    # Default values
    container_width = "1200px"
    spacing = "1rem"
    header_style = "Simple header with logo and navigation"
    footer_style = "Basic footer with copyright information"
    
    # Try to find container width
    container_pattern = r'(?:\.container|\.wrapper|\.content|main|#main)\s*{[^}]*(?:max-)?width\s*:\s*([^;]+)'
    container_match = re.search(container_pattern, css_content)
    if container_match:
        container_width = container_match.group(1).strip()
    
    # Try to find spacing
    spacing_pattern = r'(?:\.container|\.wrapper|\.content|body|:root)\s*{[^}]*(?:padding|margin)\s*:\s*([^;]+)'
    spacing_match = re.search(spacing_pattern, css_content)
    if spacing_match:
        spacing = spacing_match.group(1).strip()
    
    # Analyze header
    header = soup.find('header')
    if header:
        nav = header.find('nav')
        logo = header.find('img') or header.find(class_=re.compile(r'logo', re.I))
        
        if logo and nav:
            header_style = "Header with logo and navigation menu"
        elif logo:
            header_style = "Simple header with logo"
        elif nav:
            header_style = "Header with navigation menu"
    
    # Analyze footer
    footer = soup.find('footer')
    if footer:
        has_copyright = bool(re.search(r'copyright|©', footer.get_text(), re.I))
        has_social = bool(footer.find(class_=re.compile(r'social', re.I)))
        has_links = len(footer.find_all('a')) > 1
        
        if has_copyright and has_social and has_links:
            footer_style = "Comprehensive footer with copyright, social links, and navigation"
        elif has_copyright and has_links:
            footer_style = "Standard footer with copyright and links"
        elif has_copyright:
            footer_style = "Simple footer with copyright"
    
    return {
        "containerWidth": container_width,
        "spacing": spacing,
        "headerStyle": header_style,
        "footerStyle": footer_style
    }

def extract_components(soup, css_content):
    """Extract component styles from HTML and CSS."""
    # Default values
    button_style = "Standard rounded buttons with hover effect"
    link_style = "Underlined links with color change on hover"
    card_style = "Simple bordered cards with padding"
    
    # Analyze buttons
    button_selector = r'(?:\.btn|button|input\[type="submit"\]|\.button)\s*{([^}]*)}'
    button_match = re.search(button_selector, css_content)
    if button_match:
        button_props = button_match.group(1)
        
        if 'border-radius' in button_props:
            radius_match = re.search(r'border-radius\s*:\s*([^;]+)', button_props)
            radius = radius_match.group(1) if radius_match else "0"
            
            if '0' in radius:
                button_style = "Square buttons"
            elif 'px' in radius and int(re.search(r'(\d+)px', radius).group(1)) < 5:
                button_style = "Slightly rounded buttons"
            elif 'px' in radius and int(re.search(r'(\d+)px', radius).group(1)) >= 20:
                button_style = "Pill-shaped buttons"
            else:
                button_style = "Rounded buttons"
        
        if 'box-shadow' in button_props:
            button_style += " with shadow effect"
        
        if 'transition' in button_props or ':hover' in css_content:
            button_style += " and hover animation"
    
    # Analyze links
    link_selector = r'a\s*{([^}]*)}'
    link_match = re.search(link_selector, css_content)
    if link_match:
        link_props = link_match.group(1)
        
        if 'text-decoration' in link_props:
            if 'none' in link_props:
                link_style = "Non-underlined links"
            else:
                link_style = "Underlined links"
        
        if 'transition' in link_props or 'a:hover' in css_content:
            link_style += " with hover effect"
    
    # Analyze cards or similar container elements
    card_selector = r'(?:\.card|\.box|\.container|\.panel)\s*{([^}]*)}'
    card_match = re.search(card_selector, css_content)
    if card_match:
        card_props = card_match.group(1)
        
        if 'border' in card_props:
            card_style = "Bordered cards"
        elif 'box-shadow' in card_props:
            card_style = "Cards with shadow"
        else:
            card_style = "Simple cards"
        
        if 'border-radius' in card_props:
            card_style += " with rounded corners"
        
        if 'padding' in card_props:
            card_style += " and internal padding"
    
    return {
        "buttonStyle": button_style,
        "linkStyle": link_style,
        "cardStyle": card_style
    }
