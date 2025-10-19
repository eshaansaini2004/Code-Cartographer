"""
Dependency Analyzer Service - Builds cross-file dependency graphs

This service analyzes relationships between files:
- Maps imports to actual file paths
- Builds bidirectional dependency graph
- Detects circular dependencies
- Identifies orphaned files
"""

import os
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional
from collections import defaultdict


def normalize_import_path(import_statement: str, file_path: str, project_root: str) -> Optional[str]:
    """
    Convert an import statement to an actual file path.
    
    Args:
        import_statement: The import string (e.g., 'services.parser_service' or './utils')
        file_path: Path of the file containing the import
        project_root: Root directory of the project
        
    Returns:
        Normalized file path or None if not found
    """
    project_path = Path(project_root).resolve()
    current_file = Path(file_path).resolve()
    current_dir = current_file.parent
    
    # Handle relative imports (JavaScript/TypeScript style)
    if import_statement.startswith('.'):
        # Remove leading dots and convert to path
        parts = import_statement.lstrip('.').split('/')
        target_path = current_dir
        
        # Go up directories for each extra dot
        dots = len(import_statement) - len(import_statement.lstrip('.'))
        for _ in range(dots - 1):
            target_path = target_path.parent
        
        # Join with the rest of the path
        for part in parts:
            if part:
                target_path = target_path / part
        
        # Try different extensions
        for ext in ['.py', '.js', '.ts', '.jsx', '.tsx', '']:
            test_path = target_path.with_suffix(ext)
            if test_path.exists() and test_path.is_file():
                return str(test_path)
            
            # Try as directory with __init__.py or index.js
            if (target_path / '__init__.py').exists():
                return str(target_path / '__init__.py')
            for index_file in ['index.js', 'index.ts', 'index.jsx', 'index.tsx']:
                if (target_path / index_file).exists():
                    return str(target_path / index_file)
    
    # Handle absolute imports (Python style)
    else:
        # Convert dots to path separators
        parts = import_statement.split('.')
        target_path = project_path / Path(*parts)
        
        # Try different extensions
        for ext in ['.py', '.js', '.ts']:
            test_path = target_path.with_suffix(ext)
            if test_path.exists() and test_path.is_file():
                return str(test_path)
        
        # Try as directory with __init__.py
        if (target_path / '__init__.py').exists():
            return str(target_path / '__init__.py')
    
    return None


def build_dependency_graph(batch_analysis: Dict, project_root: str) -> Dict:
    """
    Build a dependency graph from batch analysis results.
    
    Args:
        batch_analysis: Results from batch_analyzer.analyze_project()
        project_root: Root directory of the project
        
    Returns:
        Dependency graph with nodes and edges
    """
    # Initialize graph structure
    files_info = {}
    edges = []
    
    # First pass: collect all files and their exports
    for file_result in batch_analysis['files']:
        if file_result['status'] != 'success':
            continue
        
        file_path = file_result['file_path']
        analysis = file_result['analysis']
        
        files_info[file_path] = {
            'file_path': file_path,
            'file_name': file_result['file_name'],
            'imports': analysis['imports'],
            'imports_resolved': [],  # Will be filled in second pass
            'imported_by': [],  # Will be filled in second pass
            'exports': analysis['definitions'],  # Functions defined in this file
            'calls': analysis['calls']
        }
    
    # Second pass: resolve imports and build edges
    for file_path, file_info in files_info.items():
        for import_stmt in file_info['imports']:
            resolved_path = normalize_import_path(import_stmt, file_path, project_root)
            
            if resolved_path and resolved_path in files_info:
                # Add resolved import
                file_info['imports_resolved'].append(resolved_path)
                
                # Add to imported_by list of the target file
                files_info[resolved_path]['imported_by'].append(file_path)
                
                # Add edge to graph
                edges.append({
                    'source': file_path,
                    'target': resolved_path,
                    'import_statement': import_stmt
                })
    
    # Build nodes list with metadata
    nodes = []
    for file_path, info in files_info.items():
        rel_path = os.path.relpath(file_path, project_root)
        nodes.append({
            'id': file_path,
            'label': rel_path,
            'file_name': info['file_name'],
            'exports_count': len(info['exports']),
            'imports_count': len(info['imports_resolved']),
            'imported_by_count': len(info['imported_by']),
            'calls_count': len(info['calls'])
        })
    
    return {
        'files': files_info,
        'graph': {
            'nodes': nodes,
            'edges': edges
        }
    }


def detect_circular_dependencies(dependency_graph: Dict) -> List[List[str]]:
    """
    Detect circular dependencies in the dependency graph.
    
    Args:
        dependency_graph: Graph from build_dependency_graph()
        
    Returns:
        List of circular dependency chains
    """
    files_info = dependency_graph['files']
    circular_deps = []
    
    def find_cycles(start_file, current_file, visited, path):
        """DFS to find cycles."""
        if current_file in path:
            # Found a cycle
            cycle_start = path.index(current_file)
            cycle = path[cycle_start:] + [current_file]
            if cycle not in circular_deps and list(reversed(cycle)) not in circular_deps:
                circular_deps.append(cycle)
            return
        
        if current_file in visited:
            return
        
        visited.add(current_file)
        path.append(current_file)
        
        # Follow imports
        if current_file in files_info:
            for imported_file in files_info[current_file]['imports_resolved']:
                find_cycles(start_file, imported_file, visited, path[:])
    
    # Check each file for cycles
    for file_path in files_info.keys():
        find_cycles(file_path, file_path, set(), [])
    
    return circular_deps


def find_orphaned_files(dependency_graph: Dict) -> List[str]:
    """
    Find files that are not imported by any other file.
    
    Args:
        dependency_graph: Graph from build_dependency_graph()
        
    Returns:
        List of orphaned file paths
    """
    files_info = dependency_graph['files']
    orphaned = []
    
    for file_path, info in files_info.items():
        # A file is orphaned if nothing imports it
        # (but it might still be an entry point)
        if len(info['imported_by']) == 0:
            orphaned.append(file_path)
    
    return orphaned


def find_hub_files(dependency_graph: Dict, top_n: int = 10) -> List[Tuple[str, int]]:
    """
    Find the most imported files (hub files).
    
    Args:
        dependency_graph: Graph from build_dependency_graph()
        top_n: Number of top files to return
        
    Returns:
        List of (file_path, import_count) tuples
    """
    files_info = dependency_graph['files']
    
    files_with_counts = [
        (file_path, len(info['imported_by']))
        for file_path, info in files_info.items()
    ]
    
    # Sort by import count descending
    files_with_counts.sort(key=lambda x: x[1], reverse=True)
    
    return files_with_counts[:top_n]


def analyze_dependencies(batch_analysis: Dict, project_root: str) -> Dict:
    """
    Complete dependency analysis of a project.
    
    Args:
        batch_analysis: Results from batch_analyzer.analyze_project()
        project_root: Root directory of the project
        
    Returns:
        Complete dependency analysis including graph, circular deps, orphans, hubs
    """
    # Build dependency graph
    dep_graph = build_dependency_graph(batch_analysis, project_root)
    
    # Detect issues
    circular_deps = detect_circular_dependencies(dep_graph)
    orphaned_files = find_orphaned_files(dep_graph)
    hub_files = find_hub_files(dep_graph)
    
    # Calculate statistics
    total_files = len(dep_graph['files'])
    total_edges = len(dep_graph['graph']['edges'])
    
    files_with_imports = sum(
        1 for info in dep_graph['files'].values()
        if len(info['imports_resolved']) > 0
    )
    
    files_being_imported = sum(
        1 for info in dep_graph['files'].values()
        if len(info['imported_by']) > 0
    )
    
    return {
        'dependency_graph': dep_graph,
        'circular_dependencies': circular_deps,
        'orphaned_files': orphaned_files,
        'hub_files': hub_files,
        'statistics': {
            'total_files': total_files,
            'total_dependencies': total_edges,
            'files_with_imports': files_with_imports,
            'files_being_imported': files_being_imported,
            'circular_dependency_count': len(circular_deps),
            'orphaned_file_count': len(orphaned_files)
        }
    }


def get_dependency_summary(dep_analysis: Dict, project_root: str) -> str:
    """
    Generate a human-readable summary of dependency analysis.
    
    Args:
        dep_analysis: Results from analyze_dependencies()
        project_root: Root directory of the project
        
    Returns:
        Formatted summary string
    """
    stats = dep_analysis['statistics']
    
    summary = f"""
{'='*80}
DEPENDENCY ANALYSIS SUMMARY
{'='*80}

📊 Overall Statistics:
  • Total Files: {stats['total_files']}
  • Total Dependencies: {stats['total_dependencies']}
  • Files with Imports: {stats['files_with_imports']}
  • Files Being Imported: {stats['files_being_imported']}

"""
    
    # Hub files
    if dep_analysis['hub_files']:
        summary += "\n🌟 Hub Files (Most Imported):\n"
        for i, (file_path, count) in enumerate(dep_analysis['hub_files'][:5], 1):
            rel_path = os.path.relpath(file_path, project_root)
            summary += f"  {i}. {rel_path:50s} (imported by {count} files)\n"
    
    # Circular dependencies
    if dep_analysis['circular_dependencies']:
        summary += f"\n⚠️  Circular Dependencies Found: {len(dep_analysis['circular_dependencies'])}\n"
        for i, cycle in enumerate(dep_analysis['circular_dependencies'][:3], 1):
            cycle_names = [os.path.basename(f) for f in cycle]
            summary += f"  {i}. {' → '.join(cycle_names)}\n"
        if len(dep_analysis['circular_dependencies']) > 3:
            summary += f"  ... and {len(dep_analysis['circular_dependencies']) - 3} more\n"
    else:
        summary += "\n✅ No Circular Dependencies Found\n"
    
    # Orphaned files
    if dep_analysis['orphaned_files']:
        summary += f"\n📌 Orphaned Files (Not Imported): {len(dep_analysis['orphaned_files'])}\n"
        for i, file_path in enumerate(dep_analysis['orphaned_files'][:5], 1):
            rel_path = os.path.relpath(file_path, project_root)
            summary += f"  {i}. {rel_path}\n"
        if len(dep_analysis['orphaned_files']) > 5:
            summary += f"  ... and {len(dep_analysis['orphaned_files']) - 5} more\n"
    
    summary += "\n" + "=" * 80 + "\n"
    
    return summary

