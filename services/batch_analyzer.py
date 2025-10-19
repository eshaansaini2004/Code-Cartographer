"""
Batch Analyzer Service - Analyzes entire projects

This service handles batch processing of multiple code files:
- Recursively scans directories
- Processes files in parallel
- Caches results for performance
- Aggregates project-level statistics
"""

import os
import json
from pathlib import Path
from typing import List, Dict, Set, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from services.parser_service import analyze_code


# Default patterns to exclude
DEFAULT_EXCLUDE_PATTERNS = {
    'node_modules', 'venv', 'env', '__pycache__', '.git', 
    'dist', 'build', 'out', '.vscode', '.idea', 'coverage',
    'vendor', 'target', 'bin', 'obj'
}

# Supported file extensions
SUPPORTED_EXTENSIONS = {'.py', '.js', '.ts', '.jsx', '.tsx'}


def scan_directory(
    directory_path: str, 
    exclude_patterns: Optional[Set[str]] = None
) -> List[str]:
    """
    Recursively scan a directory for supported code files.
    
    Args:
        directory_path: Root directory to scan
        exclude_patterns: Set of directory/file patterns to exclude
        
    Returns:
        List of file paths to analyze
    """
    if exclude_patterns is None:
        exclude_patterns = DEFAULT_EXCLUDE_PATTERNS
    else:
        exclude_patterns = DEFAULT_EXCLUDE_PATTERNS.union(exclude_patterns)
    
    code_files = []
    directory = Path(directory_path).resolve()
    
    for root, dirs, files in os.walk(directory):
        # Filter out excluded directories
        dirs[:] = [d for d in dirs if d not in exclude_patterns]
        
        # Check if any part of the path contains excluded patterns
        root_path = Path(root)
        should_skip = any(
            excluded in root_path.parts 
            for excluded in exclude_patterns
        )
        
        if should_skip:
            continue
        
        # Find supported code files
        for file in files:
            file_path = Path(root) / file
            if file_path.suffix in SUPPORTED_EXTENSIONS:
                code_files.append(str(file_path))
    
    return sorted(code_files)


def analyze_single_file(file_path: str) -> Dict:
    """
    Analyze a single file and return results with metadata.
    
    Args:
        file_path: Path to the file to analyze
        
    Returns:
        Dictionary with analysis results and metadata
    """
    try:
        analysis_results = analyze_code(file_path)
        
        # Add metadata
        file_stats = os.stat(file_path)
        
        return {
            'file_path': file_path,
            'file_name': os.path.basename(file_path),
            'file_size': file_stats.st_size,
            'extension': os.path.splitext(file_path)[1],
            'analysis': analysis_results,
            'status': 'success',
            'error': None
        }
    except Exception as e:
        return {
            'file_path': file_path,
            'file_name': os.path.basename(file_path),
            'status': 'error',
            'error': str(e),
            'analysis': None
        }


def analyze_project(
    directory_path: str,
    exclude_patterns: Optional[Set[str]] = None,
    max_workers: int = 4,
    progress_callback=None
) -> Dict:
    """
    Analyze all code files in a project directory.
    
    Args:
        directory_path: Root directory of the project
        exclude_patterns: Additional patterns to exclude
        max_workers: Number of parallel workers
        progress_callback: Optional callback function for progress updates
        
    Returns:
        Dictionary with project-wide analysis results
    """
    # Scan for files
    code_files = scan_directory(directory_path, exclude_patterns)
    
    if not code_files:
        return {
            'status': 'error',
            'message': 'No supported code files found in directory',
            'files_analyzed': 0
        }
    
    print(f"\n📁 Found {len(code_files)} code files to analyze")
    
    # Analyze files in parallel
    results = []
    successful = 0
    failed = 0
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        future_to_file = {
            executor.submit(analyze_single_file, file_path): file_path 
            for file_path in code_files
        }
        
        # Process completed tasks
        for i, future in enumerate(as_completed(future_to_file), 1):
            result = future.result()
            results.append(result)
            
            if result['status'] == 'success':
                successful += 1
            else:
                failed += 1
            
            # Progress callback
            if progress_callback:
                progress_callback(i, len(code_files), result['file_name'])
            else:
                print(f"  [{i}/{len(code_files)}] {result['file_name']}: {result['status']}")
    
    # Aggregate statistics
    total_imports = sum(
        len(r['analysis']['imports']) 
        for r in results 
        if r['status'] == 'success'
    )
    total_definitions = sum(
        len(r['analysis']['definitions']) 
        for r in results 
        if r['status'] == 'success'
    )
    total_calls = sum(
        len(r['analysis']['calls']) 
        for r in results 
        if r['status'] == 'success'
    )
    
    # Build project analysis
    project_analysis = {
        'project_path': directory_path,
        'analyzed_at': datetime.now().isoformat(),
        'statistics': {
            'total_files': len(code_files),
            'successful': successful,
            'failed': failed,
            'total_imports': total_imports,
            'total_definitions': total_definitions,
            'total_calls': total_calls
        },
        'files': results,
        'status': 'success'
    }
    
    return project_analysis


def save_analysis_cache(results: Dict, cache_file: str) -> None:
    """
    Save analysis results to a cache file.
    
    Args:
        results: Analysis results dictionary
        cache_file: Path to cache file
    """
    cache_path = Path(cache_file)
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(cache_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    
    print(f"💾 Analysis cached to: {cache_file}")


def load_analysis_cache(cache_file: str) -> Optional[Dict]:
    """
    Load analysis results from a cache file.
    
    Args:
        cache_file: Path to cache file
        
    Returns:
        Cached analysis results or None if cache doesn't exist/is invalid
    """
    if not os.path.exists(cache_file):
        return None
    
    try:
        with open(cache_file, 'r', encoding='utf-8') as f:
            results = json.load(f)
        
        print(f"📂 Loaded cached analysis from: {cache_file}")
        return results
    except Exception as e:
        print(f"⚠️  Cache file invalid: {e}")
        return None


def get_project_summary(project_analysis: Dict, dependency_analysis: Dict = None) -> Dict:
    """
    Generate a human-readable summary of project analysis.
    
    Args:
        project_analysis: Project analysis dictionary
        dependency_analysis: Optional dependency analysis dictionary
        
    Returns:
        Dictionary with summary statistics
    """
    stats = project_analysis['statistics']
    
    # Create summary dict for API
    summary_dict = {
        'total_files': stats['total_files'],
        'total_definitions': stats['total_definitions'],
        'total_imports': stats['total_imports'],
        'total_calls': stats['total_calls'],
        'total_dependencies': dependency_analysis['statistics']['total_dependencies'] if dependency_analysis else 0
    }
    
    return summary_dict

