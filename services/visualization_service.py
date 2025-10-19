"""
Visualization Service - Creates interactive dependency graphs

This service generates visual representations of code dependencies:
- Interactive network diagrams using Plotly
- Node sizing based on metrics
- Color coding by file type
- Export to HTML, PNG, SVG, JSON
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Optional
import networkx as nx
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def create_network_graph(dependency_analysis: Dict, project_root: str) -> nx.DiGraph:
    """
    Create a NetworkX directed graph from dependency analysis.
    
    Args:
        dependency_analysis: Results from dependency_analyzer.analyze_dependencies()
        project_root: Root directory of the project
        
    Returns:
        NetworkX directed graph
    """
    G = nx.DiGraph()
    
    dep_graph = dependency_analysis['dependency_graph']
    files_info = dep_graph['files']
    
    # Add nodes with attributes
    for node in dep_graph['graph']['nodes']:
        file_path = node['id']
        rel_path = os.path.relpath(file_path, project_root)
        
        G.add_node(
            file_path,
            label=node['label'],
            file_name=node['file_name'],
            exports_count=node['exports_count'],
            imports_count=node['imports_count'],
            imported_by_count=node['imported_by_count'],
            calls_count=node['calls_count'],
            rel_path=rel_path
        )
    
    # Add edges
    for edge in dep_graph['graph']['edges']:
        G.add_edge(
            edge['source'],
            edge['target'],
            import_statement=edge.get('import_statement', '')
        )
    
    return G


def get_node_color(file_path: str) -> str:
    """
    Get color for node based on file type.
    
    Args:
        file_path: Path to the file
        
    Returns:
        Color string for the node
    """
    ext = os.path.splitext(file_path)[1]
    color_map = {
        '.py': '#3776ab',  # Python blue
        '.js': '#f7df1e',  # JavaScript yellow
        '.ts': '#3178c6',  # TypeScript blue
        '.jsx': '#61dafb', # React cyan
        '.tsx': '#61dafb'  # React cyan
    }
    return color_map.get(ext, '#888888')


def generate_dependency_graph(
    dependency_analysis: Dict,
    project_root: str,
    layout: str = 'spring',
    width: int = 1200,
    height: int = 800
) -> go.Figure:
    """
    Generate an interactive dependency graph visualization.
    
    Args:
        dependency_analysis: Results from dependency_analyzer.analyze_dependencies()
        project_root: Root directory of the project
        layout: Layout algorithm ('spring', 'circular', 'kamada_kawai')
        width: Width of the visualization
        height: Height of the visualization
        
    Returns:
        Plotly Figure object
    """
    # Create NetworkX graph
    G = create_network_graph(dependency_analysis, project_root)
    
    if len(G.nodes()) == 0:
        # Return empty figure if no nodes
        fig = go.Figure()
        fig.add_annotation(
            text="No dependencies to visualize",
            showarrow=False,
            font=dict(size=20)
        )
        return fig
    
    # Choose layout algorithm
    if layout == 'circular':
        pos = nx.circular_layout(G)
    elif layout == 'kamada_kawai':
        pos = nx.kamada_kawai_layout(G)
    else:  # spring (default)
        pos = nx.spring_layout(G, k=0.5, iterations=50)
    
    # Create edge traces
    edge_traces = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        
        edge_trace = go.Scatter(
            x=[x0, x1, None],
            y=[y0, y1, None],
            mode='lines',
            line=dict(width=0.5, color='#888'),
            hoverinfo='none',
            showlegend=False
        )
        edge_traces.append(edge_trace)
    
    # Create node trace
    node_x = []
    node_y = []
    node_text = []
    node_color = []
    node_size = []
    
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        
        attrs = G.nodes[node]
        
        # Create hover text
        hover_text = f"<b>{attrs['file_name']}</b><br>"
        hover_text += f"Path: {attrs['rel_path']}<br>"
        hover_text += f"Exports: {attrs['exports_count']} functions<br>"
        hover_text += f"Imports: {attrs['imports_count']} files<br>"
        hover_text += f"Imported by: {attrs['imported_by_count']} files<br>"
        hover_text += f"Calls: {attrs['calls_count']}<br>"
        node_text.append(hover_text)
        
        # Color by file type
        node_color.append(get_node_color(node))
        
        # Size by number of functions + imports
        size = 10 + (attrs['exports_count'] * 2) + attrs['imported_by_count']
        node_size.append(min(size, 50))  # Cap at 50
    
    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode='markers+text',
        hoverinfo='text',
        text=[G.nodes[node]['file_name'] for node in G.nodes()],
        hovertext=node_text,
        textposition='top center',
        textfont=dict(size=8),
        marker=dict(
            size=node_size,
            color=node_color,
            line=dict(width=2, color='white')
        ),
        showlegend=False
    )
    
    # Create figure
    fig = go.Figure()
    
    # Add edges first (so they're behind nodes)
    for edge_trace in edge_traces:
        fig.add_trace(edge_trace)
    
    # Add nodes
    fig.add_trace(node_trace)
    
    # Update layout
    fig.update_layout(
        title=dict(
            text=f"Code Dependency Graph: {os.path.basename(project_root)}",
            x=0.5,
            xanchor='center'
        ),
        showlegend=False,
        hovermode='closest',
        margin=dict(b=20, l=5, r=5, t=40),
        width=width,
        height=height,
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        plot_bgcolor='#fafafa'
    )
    
    return fig


def export_graph_html(
    fig: go.Figure,
    output_path: str,
    include_plotlyjs: str = 'cdn'
) -> None:
    """
    Export graph to interactive HTML file.
    
    Args:
        fig: Plotly Figure object
        output_path: Path to save HTML file
        include_plotlyjs: How to include Plotly.js ('cdn', 'inline', etc.)
    """
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    fig.write_html(
        str(output_file),
        include_plotlyjs=include_plotlyjs,
        config={'displayModeBar': True, 'responsive': True}
    )
    
    print(f"📊 Interactive graph saved to: {output_file}")


def export_graph_image(
    fig: go.Figure,
    output_path: str,
    format: str = 'png',
    width: int = 1920,
    height: int = 1080
) -> None:
    """
    Export graph to static image file (PNG or SVG).
    
    Args:
        fig: Plotly Figure object
        output_path: Path to save image file
        format: Image format ('png' or 'svg')
        width: Image width in pixels
        height: Image height in pixels
    """
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    if format.lower() == 'svg':
        fig.write_image(str(output_file), format='svg', width=width, height=height)
    else:
        fig.write_image(str(output_file), format='png', width=width, height=height)
    
    print(f"🖼️  Static image saved to: {output_file}")


def export_graph_json(
    dependency_analysis: Dict,
    output_path: str
) -> None:
    """
    Export graph data as JSON for custom rendering.
    
    Args:
        dependency_analysis: Results from dependency_analyzer.analyze_dependencies()
        output_path: Path to save JSON file
    """
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Export just the graph structure
    graph_data = {
        'nodes': dependency_analysis['dependency_graph']['graph']['nodes'],
        'edges': dependency_analysis['dependency_graph']['graph']['edges'],
        'statistics': dependency_analysis['statistics']
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(graph_data, f, indent=2)
    
    print(f"📄 Graph JSON saved to: {output_file}")


def create_statistics_visualization(
    dependency_analysis: Dict,
    batch_analysis: Dict,
    project_root: str
) -> go.Figure:
    """
    Create a dashboard-style statistics visualization.
    
    Args:
        dependency_analysis: Results from dependency_analyzer.analyze_dependencies()
        batch_analysis: Results from batch_analyzer.analyze_project()
        project_root: Root directory of the project
        
    Returns:
        Plotly Figure with multiple subplots
    """
    stats = batch_analysis['statistics']
    dep_stats = dependency_analysis['statistics']
    
    # Create subplots
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            'Files by Type',
            'Top Files by Function Count',
            'Dependency Statistics',
            'File Relationships'
        ),
        specs=[[{'type': 'pie'}, {'type': 'bar'}],
               [{'type': 'bar'}, {'type': 'bar'}]]
    )
    
    # 1. Files by type (Pie chart)
    files_by_type = {}
    for file_result in batch_analysis['files']:
        ext = file_result.get('extension', 'unknown')
        files_by_type[ext] = files_by_type.get(ext, 0) + 1
    
    fig.add_trace(
        go.Pie(
            labels=list(files_by_type.keys()),
            values=list(files_by_type.values()),
            hole=0.3
        ),
        row=1, col=1
    )
    
    # 2. Top files by function count (Bar chart)
    sorted_files = sorted(
        [f for f in batch_analysis['files'] if f['status'] == 'success'],
        key=lambda x: len(x['analysis']['definitions']),
        reverse=True
    )[:10]
    
    file_names = [os.path.basename(f['file_path']) for f in sorted_files]
    func_counts = [len(f['analysis']['definitions']) for f in sorted_files]
    
    fig.add_trace(
        go.Bar(x=func_counts, y=file_names, orientation='h'),
        row=1, col=2
    )
    
    # 3. Dependency statistics (Bar chart)
    dep_data = {
        'Total Files': dep_stats['total_files'],
        'Total Dependencies': dep_stats['total_dependencies'],
        'Files with Imports': dep_stats['files_with_imports'],
        'Files Being Imported': dep_stats['files_being_imported']
    }
    
    fig.add_trace(
        go.Bar(x=list(dep_data.keys()), y=list(dep_data.values())),
        row=2, col=1
    )
    
    # 4. File relationships (Bar chart)
    relationship_data = {
        'Circular Deps': dep_stats['circular_dependency_count'],
        'Orphaned Files': dep_stats['orphaned_file_count'],
        'Hub Files (>3 deps)': len([
            h for h in dependency_analysis['hub_files'] 
            if h[1] > 3
        ])
    }
    
    fig.add_trace(
        go.Bar(x=list(relationship_data.keys()), y=list(relationship_data.values())),
        row=2, col=2
    )
    
    # Update layout
    fig.update_layout(
        title_text=f"Project Statistics: {os.path.basename(project_root)}",
        showlegend=False,
        height=800
    )
    
    return fig

