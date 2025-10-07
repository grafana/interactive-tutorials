#!/usr/bin/env python3
"""
HTML validation script for GitHub Actions workflow.
Validates HTML files for well-formedness and basic structure.
"""

import html.parser
import sys
import re
import os

class HTMLValidator(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.errors = []
        self.warnings = []
    
    def error(self, message):
        self.errors.append(message)
    
    def handle_decl(self, decl):
        # Handle DOCTYPE declarations
        pass
    
    def handle_starttag(self, tag, attrs):
        # Check for common issues
        if tag.lower() in ['script', 'style']:
            # These tags might have content that's not valid HTML
            pass
    
    def handle_endtag(self, tag):
        pass
    
    def handle_data(self, data):
        pass
    
    def handle_comment(self, data):
        pass
    
    def handle_entityref(self, name):
        pass
    
    def handle_charref(self, name):
        pass
    
    def handle_pi(self, data):
        pass

def validate_html_file(filepath):
    """Validate HTML syntax using Python's html.parser"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Basic checks
        if not content.strip():
            print('❌ Error: File is empty')
            return False
        
        # Check for basic HTML structure
        if '<html' not in content.lower() and '<!doctype' not in content.lower():
            print('⚠️  Warning: File does not appear to contain HTML structure')
        
        # Parse with HTML parser
        validator = HTMLValidator()
        try:
            validator.feed(content)
            validator.close()
        except Exception as e:
            print(f'❌ Error: HTML parsing failed - {e}')
            return False
        
        if validator.errors:
            print('❌ Errors found:')
            for error in validator.errors:
                print(f'  - {error}')
            return False
        
        print('✅ HTML is well-formed')
        return True
        
    except Exception as e:
        print(f'❌ Error reading file: {e}')
        return False

def check_html_structure(filepath):
    """Check basic HTML structure requirements"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        issues = []
        
        # Check for DOCTYPE or html tag
        if not re.search(r'<!DOCTYPE|<html', content, re.IGNORECASE):
            issues.append('Missing DOCTYPE declaration or <html> tag')
        
        # Check for head and body tags
        if not re.search(r'<head[^>]*>', content, re.IGNORECASE):
            issues.append('Missing <head> tag')
        
        if not re.search(r'<body[^>]*>', content, re.IGNORECASE):
            issues.append('Missing <body> tag')
        
        # Check for proper closing tags
        if re.search(r'<html[^>]*>', content, re.IGNORECASE) and not re.search(r'</html>', content, re.IGNORECASE):
            issues.append('Missing closing </html> tag')
        
        if re.search(r'<head[^>]*>', content, re.IGNORECASE) and not re.search(r'</head>', content, re.IGNORECASE):
            issues.append('Missing closing </head> tag')
        
        if re.search(r'<body[^>]*>', content, re.IGNORECASE) and not re.search(r'</body>', content, re.IGNORECASE):
            issues.append('Missing closing </body> tag')
        
        # Check for title tag in head
        if re.search(r'<head[^>]*>', content, re.IGNORECASE) and not re.search(r'<title[^>]*>', content, re.IGNORECASE):
            issues.append('Missing <title> tag in <head>')
        
        if issues:
            print('⚠️  Structure issues found:')
            for issue in issues:
                print(f'  - {issue}')
            return False
        else:
            print('✅ HTML structure looks good')
            return True
            
    except Exception as e:
        print(f'❌ Error checking structure: {e}')
        return False

def main():
    if len(sys.argv) != 3:
        print("Usage: python validate_html.py <filepath> <validation_type>")
        print("validation_type: 'syntax' or 'structure'")
        sys.exit(1)
    
    filepath = sys.argv[1]
    validation_type = sys.argv[2]
    
    if not os.path.exists(filepath):
        print(f'❌ Error: File {filepath} does not exist')
        sys.exit(1)
    
    if validation_type == 'syntax':
        success = validate_html_file(filepath)
    elif validation_type == 'structure':
        success = check_html_structure(filepath)
    else:
        print("Invalid validation type. Use 'syntax' or 'structure'")
        sys.exit(1)
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
