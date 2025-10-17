#!/usr/bin/env python3
"""
JSON validation script for GitHub Actions workflow.
Validates index.json for well-formedness and basic structure.
"""

import json
import sys
import os

def validate_json_syntax(filepath):
    """Validate JSON syntax using Python's json.tool"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Basic checks
        if not content.strip():
            print('❌ Error: File is empty')
            return False
        
        # Validate JSON syntax
        try:
            json.loads(content)
        except json.JSONDecodeError as e:
            print(f'❌ Error: Invalid JSON syntax - {e}')
            return False
        
        print('✅ JSON is well-formed')
        return True
        
    except Exception as e:
        print(f'❌ Error reading file: {e}')
        return False

def validate_json_structure(filepath):
    """Check JSON structure requirements"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        issues = []
        
        # Check if it's a dictionary
        if not isinstance(data, dict):
            issues.append('Root element must be an object')
        
        # Check if 'rules' key exists
        if 'rules' not in data:
            issues.append('Missing required "rules" key')
        else:
            # Check if 'rules' is a list
            if not isinstance(data['rules'], list):
                issues.append('"rules" must be an array')
            else:
                # Validate each rule has required fields
                required_fields = ['title', 'url', 'description', 'type', 'match']
                for i, rule in enumerate(data['rules']):
                    if not isinstance(rule, dict):
                        issues.append(f'Rule {i} must be an object')
                    else:
                        for field in required_fields:
                            if field not in rule:
                                issues.append(f'Rule {i} missing required field "{field}"')
        
        if issues:
            print('❌ Structure issues found:')
            for issue in issues:
                print(f'  - {issue}')
            return False
        else:
            print('✅ JSON structure looks good')
            print(f'✅ Found {len(data["rules"])} valid rule(s)')
            return True
            
    except Exception as e:
        print(f'❌ Error checking structure: {e}')
        return False

def main():
    if len(sys.argv) != 2:
        print("Usage: python validate_json.py <filepath>")
        sys.exit(1)
    
    filepath = sys.argv[1]
    
    if not os.path.exists(filepath):
        print(f'❌ Error: File {filepath} does not exist')
        sys.exit(1)
    
    # First validate syntax
    if not validate_json_syntax(filepath):
        sys.exit(1)
    
    # Then validate structure
    if not validate_json_structure(filepath):
        sys.exit(1)
    
    print('🎉 All validations passed! index.json is well-formed and properly structured.')
    sys.exit(0)

if __name__ == "__main__":
    main()
