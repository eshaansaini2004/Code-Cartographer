"""
AI Service - Uses Google Gemini to generate human-readable summaries

This service takes the structured analysis from the parser and uses AI to generate
a comprehensive, human-readable summary of the code file.
"""

import os
from google import genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def get_ai_summary_sync(file_path: str, code_content: str, analysis_results: dict) -> str:
    """
    Generate an AI-powered summary of a code file.
    
    Args:
        file_path: Path to the code file being analyzed
        code_content: The full content of the code file
        analysis_results: Dictionary with 'imports', 'definitions', and 'calls' lists
        
    Returns:
        A formatted string with the AI-generated analysis
    """
    # Initialize Gemini client with new API
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key or api_key == 'your-api-key-here':
        raise ValueError(
            "Gemini API key not found. Please set GEMINI_API_KEY in your .env file.\n"
            "Get your key from: https://aistudio.google.com/app/apikey"
        )
    
    client = genai.Client(api_key=api_key)
    
    # Construct the detailed prompt
    imports_list = "\n".join(f"  - {imp}" for imp in analysis_results.get('imports', []))
    definitions_list = "\n".join(f"  - {defn}" for defn in analysis_results.get('definitions', []))
    calls_list = "\n".join(f"  - {call}" for call in analysis_results.get('calls', []))
    
    system_prompt = """You are a senior software engineer helping developers understand unfamiliar codebases. 
Your job is to analyze code and provide clear, concise explanations that help developers quickly understand:
1. What the code does (its purpose and responsibility)
2. What it depends on (outbound connections)
3. What depends on it (inbound connections, what this code provides to others)

Be precise, avoid jargon when possible, and focus on the most important relationships."""

    user_prompt = f"""Analyze this code file and provide a structured summary.

**File:** {file_path}

**Structural Analysis (extracted by parser):**

Imports detected:
{imports_list if imports_list else "  (none)"}

Function definitions:
{definitions_list if definitions_list else "  (none)"}

Function calls made:
{calls_list if calls_list else "  (none)"}

**Full Code Content:**
```
{code_content}
```

Please provide your analysis in the following format:

**Summary:**
[A concise, one-paragraph explanation of this file's purpose and what it does. Focus on the "why" and "what" at a high level.]

**Dependencies (Outbound):**
[A bulleted list of the key external modules, functions, or services this file relies on. Based on the imports and external calls detected above. Explain WHY each dependency is needed.]

**Key Functions (Inbound):**
[A bulleted list of the most important functions defined in this file that other parts of the codebase are likely to use. For each, briefly explain what it does and why it would be called by other code.]

If there are any notable patterns, potential issues, or architectural insights, mention them briefly at the end.
"""

    # Call Gemini API with new client
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=f"{system_prompt}\n\n{user_prompt}"
        )
        
        # Extract and return the response
        return response.text
        
    except Exception as e:
        raise Exception(f"Error calling Gemini API: {str(e)}")


def analyze_project_architecture(dependency_analysis: dict, batch_analysis: dict, project_root: str) -> str:
    """
    Generate AI-powered architecture analysis of entire project.
    
    Args:
        dependency_analysis: Results from dependency_analyzer.analyze_dependencies()
        batch_analysis: Results from batch_analyzer.analyze_project()
        project_root: Root directory of the project
        
    Returns:
        AI-generated architectural insights
    """
    # Initialize Gemini client with new API
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key or api_key == 'your-api-key-here':
        raise ValueError(
            "Gemini API key not found. Please set GEMINI_API_KEY in your .env file.\n"
            "Get your key from: https://aistudio.google.com/app/apikey"
        )
    
    client = genai.Client(api_key=api_key)
    
    # Extract key information
    stats = batch_analysis['statistics']
    dep_stats = dependency_analysis['statistics']
    hub_files = dependency_analysis['hub_files'][:5]
    orphaned = dependency_analysis['orphaned_files'][:5]
    circular = dependency_analysis['circular_dependencies'][:3]
    
    # Format hub files
    hub_list = "\n".join([
        f"  - {os.path.basename(file)} (imported by {count} files)"
        for file, count in hub_files
    ])
    
    # Format orphaned files
    orphaned_list = "\n".join([
        f"  - {os.path.basename(file)}"
        for file in orphaned
    ])
    
    # Format circular dependencies
    circular_list = "\n".join([
        f"  - {' → '.join([os.path.basename(f) for f in cycle])}"
        for cycle in circular
    ])
    
    # Get sample file contents from important files
    sample_files = []
    for file_path, _ in hub_files[:3]:
        for file_result in batch_analysis['files']:
            if file_result['file_path'] == file_path and file_result['status'] == 'success':
                sample_files.append({
                    'name': os.path.basename(file_path),
                    'imports': file_result['analysis']['imports'][:5],
                    'functions': file_result['analysis']['definitions'][:5]
                })
                break
    
    samples_text = "\n".join([
        f"\n{f['name']}:\n  Imports: {', '.join(f['imports'])}\n  Functions: {', '.join(f['functions'])}"
        for f in sample_files
    ])
    
    system_prompt = """You are a software architect helping developers understand large codebases.
Your job is to analyze the overall project structure and provide high-level architectural insights.
Focus on:
1. Main architectural patterns (MVC, microservices, layered, etc.)
2. Entry points and core modules
3. Separation of concerns and modularity
4. Potential architectural issues or improvements
5. Overall code organization strategy"""

    user_prompt = f"""Analyze this project's architecture based on the dependency analysis.

**Project:** {os.path.basename(project_root)}

**Project Statistics:**
- Total Files: {stats['total_files']}
- Total Functions: {stats['total_definitions']}
- Total Dependencies: {dep_stats['total_dependencies']}
- Files with Imports: {dep_stats['files_with_imports']}
- Circular Dependencies: {dep_stats['circular_dependency_count']}

**Hub Files (Most Depended Upon):**
{hub_list if hub_list else "  (none)"}

**Orphaned Files (Entry Points or Unused):**
{orphaned_list if orphaned_list else "  (none)"}

**Circular Dependencies Detected:**
{circular_list if circular_list else "  (none)"}

**Sample Key Files:**
{samples_text}

Please provide your architectural analysis in the following format:

**Architecture Pattern:**
[Identify the main architectural pattern(s) used in this project]

**Entry Points:**
[Identify likely entry points based on orphaned files and structure]

**Core Modules:**
[Identify the core/central modules that many files depend on]

**Separation of Concerns:**
[Evaluate how well the code is organized into logical components]

**Potential Issues:**
[List any architectural concerns like circular dependencies, tight coupling, etc.]

**Recommendations:**
[Suggest 2-3 specific improvements to the architecture]

Keep your analysis practical and actionable."""

    # Call Gemini API with new client
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=f"{system_prompt}\n\n{user_prompt}"
        )
        
        # Extract and return the response
        return response.text
        
    except Exception as e:
        raise Exception(f"Error calling Gemini API: {str(e)}")
