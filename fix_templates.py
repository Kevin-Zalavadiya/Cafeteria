import os
import re

# Define the directory containing the templates
templates_dir = os.path.join('rai', 'templates')

# Get all HTML files in the templates directory
html_files = [f for f in os.listdir(templates_dir) if f.endswith('.html')]

for html_file in html_files:
    file_path = os.path.join(templates_dir, html_file)
    
    # Read the file content
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if {% load static %} is present
    if '{% load static %}' not in content:
        # Add {% load static %} at the beginning of the file
        content = '{% load static %}\n' + content
    
    # Fix the script references
    content = content.replace('src="mail/jqBootstrapValidation.min.js"', 'src="{% static \'mail/jqBootstrapValidation.min.js\' %}"')
    content = content.replace('src="mail/contact.js"', 'src="{% static \'mail/contact.js\' %}"')
    content = content.replace('src="/static/mail/jqBootstrapValidation.min.js"', 'src="{% static \'mail/jqBootstrapValidation.min.js\' %}"')
    content = content.replace('src="/static/mail/contact.js"', 'src="{% static \'mail/contact.js\' %}"')
    
    # Write the modified content back to the file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Fixed {html_file}")

print("All templates have been fixed.")
