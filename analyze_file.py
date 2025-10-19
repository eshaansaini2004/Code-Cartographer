#!/usr/bin/env python3
"""
Simple file analyzer - bypasses the VS Code extension
Run this directly to test Code Cartographer
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.parser_service import analyze_code
from services.ai_service import get_ai_summary_sync

def main():
    if len(sys.argv) < 2:
        print("Usage: python analyze_file.py <file_path>")
        print("Example: python analyze_file.py test_example.py")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    if not os.path.exists(file_path):
        print(f"Error: File not found: {file_path}")
        sys.exit(1)
    
    print("🔍 Analyzing file with Code Cartographer...")
    print(f"📄 File: {file_path}")
    print("-" * 50)
    
    try:
        # Parse the code
        analysis_results = analyze_code(file_path)
        print(f"✓ Found {len(analysis_results['imports'])} imports")
        print(f"✓ Found {len(analysis_results['definitions'])} function definitions")
        print(f"✓ Found {len(analysis_results['calls'])} function calls")
        
        # Read file content
        with open(file_path, 'r', encoding='utf-8') as f:
            code_content = f.read()
        
        # Generate AI summary
        print("\n🤖 Generating AI summary...")
        summary = get_ai_summary_sync(file_path, code_content, analysis_results)
        
        print("\n" + "=" * 60)
        print("ANALYSIS RESULTS")
        print("=" * 60)
        print(summary)
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

