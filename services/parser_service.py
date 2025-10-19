"""
Parser Service - Uses tree-sitter to extract structural information from code

This service uses tree-sitter to deterministically parse code files and extract:
- Import statements
- Function definitions
- Function calls
"""

import os
from tree_sitter import Parser, Language
from tree_sitter_languages import get_language, get_parser


def get_parser(language: str) -> Parser:
    """
    Get a tree-sitter parser for the specified language.
    
    Args:
        language: One of 'python', 'javascript', or 'typescript'
        
    Returns:
        A configured Parser instance
    """
    # Get the language grammar
    lang = get_language(language)
    
    # Initialize and configure the parser
    parser = Parser()
    parser.set_language(lang)
    
    return parser


def analyze_code(file_path: str) -> dict:
    """
    Analyze a code file and extract structural information.
    
    Args:
        file_path: Path to the code file to analyze
        
    Returns:
        A dictionary with:
        - imports: List of imported modules/packages
        - definitions: List of function names defined in this file
        - calls: List of function names called in this file
    """
    # Determine language from file extension
    ext = os.path.splitext(file_path)[1]
    language_map = {
        '.py': 'python',
        '.js': 'javascript',
        '.ts': 'typescript',
        '.jsx': 'javascript',
        '.tsx': 'typescript'
    }
    
    language = language_map.get(ext)
    if not language:
        raise ValueError(f"Unsupported file extension: {ext}")
    
    # Get the appropriate parser
    parser = get_parser(language)
    
    # Read the file content
    with open(file_path, 'r', encoding='utf-8') as f:
        code_content = f.read()
    
    # Parse the code into a syntax tree
    tree = parser.parse(bytes(code_content, 'utf8'))
    root_node = tree.root_node
    
    # Initialize results
    imports = []
    definitions = []
    calls = []
    
    # Define language-specific queries
    if language == 'python':
        # Python import queries
        import_query = """
        (import_statement
          name: (dotted_name) @import)
        (import_from_statement
          module_name: (dotted_name) @import)
        """
        
        # Python function definitions
        def_query = """
        (function_definition
          name: (identifier) @name)
        """
        
        # Python function calls
        call_query = """
        (call
          function: (identifier) @name)
        (call
          function: (attribute
            attribute: (identifier) @name))
        """
        
    else:  # JavaScript/TypeScript
        # JS/TS import queries
        import_query = """
        (import_statement
          source: (string) @import)
        """
        
        # JS/TS function definitions
        def_query = """
        (function_declaration
          name: (identifier) @name)
        (arrow_function) @name
        (method_definition
          name: (property_identifier) @name)
        """
        
        # JS/TS function calls
        call_query = """
        (call_expression
          function: (identifier) @name)
        (call_expression
          function: (member_expression
            property: (property_identifier) @name))
        """
    
    # Execute queries and extract results
    lang = get_language(language)
    
    # Extract imports
    try:
        query = lang.query(import_query)
        captures = query.captures(root_node)
        for node, _ in captures:
            text = code_content[node.start_byte:node.end_byte]
            # Clean up the text (remove quotes for JS/TS imports)
            text = text.strip('"').strip("'")
            if text and text not in imports:
                imports.append(text)
    except Exception as e:
        print(f"Warning: Could not parse imports: {e}")
    
    # Extract function definitions
    try:
        query = lang.query(def_query)
        captures = query.captures(root_node)
        for node, _ in captures:
            text = code_content[node.start_byte:node.end_byte]
            if text and text not in definitions:
                definitions.append(text)
    except Exception as e:
        print(f"Warning: Could not parse function definitions: {e}")
    
    # Extract function calls
    try:
        query = lang.query(call_query)
        captures = query.captures(root_node)
        for node, _ in captures:
            text = code_content[node.start_byte:node.end_byte]
            if text and text not in calls and text not in definitions:
                calls.append(text)
    except Exception as e:
        print(f"Warning: Could not parse function calls: {e}")
    
    return {
        "imports": imports,
        "definitions": definitions,
        "calls": calls
    }

