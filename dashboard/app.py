"""
Code Cartographer Web Dashboard
Flask-based web interface for visualizing and exploring code analysis results
"""

import os
import sys
import json
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import threading

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.batch_analyzer import analyze_project, get_project_summary
from services.dependency_analyzer import analyze_dependencies
from services.visualization_service import generate_dependency_graph, export_graph_html
from services.ai_service import analyze_project_architecture

app = Flask(__name__)
app.config['SECRET_KEY'] = 'code-cartographer-secret-key'
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Store analysis results in memory (in production, use Redis or database)
analysis_cache = {}


@app.route('/')
def index():
    """Home page - project overview"""
    return render_template('index.html')


@app.route('/api/analyze', methods=['POST'])
def analyze_project_api():
    """
    Analyze a project directory
    POST /api/analyze
    Body: {"path": "/path/to/project", "exclude": ["node_modules", "venv"]}
    """
    data = request.json
    project_path = data.get('path')
    exclude_patterns = data.get('exclude', ['node_modules', 'venv', '__pycache__', '.git'])
    
    if not project_path or not os.path.exists(project_path):
        return jsonify({'error': 'Invalid project path'}), 400
    
    try:
        # Start analysis in background thread
        thread = threading.Thread(
            target=run_analysis,
            args=(project_path, exclude_patterns)
        )
        thread.start()
        
        return jsonify({
            'status': 'started',
            'message': 'Analysis started. Listen to WebSocket for progress.'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def run_analysis(project_path, exclude_patterns):
    """Run analysis and emit progress via WebSocket"""
    try:
        socketio.emit('analysis_progress', {
            'stage': 'scanning',
            'message': 'Scanning project files...'
        })
        
        # Batch analysis
        batch_results = analyze_project(project_path, exclude_patterns)
        
        socketio.emit('analysis_progress', {
            'stage': 'dependencies',
            'message': 'Building dependency graph...'
        })
        
        # Dependency analysis
        dep_results = analyze_dependencies(batch_results, project_path)
        
        socketio.emit('analysis_progress', {
            'stage': 'visualization',
            'message': 'Generating visualizations...'
        })
        
        # Generate graph - convert to JSON format for frontend
        from services.visualization_service import create_network_graph
        import networkx as nx
        
        # Create the network graph
        G = create_network_graph(dep_results, project_path)
        
        # Convert to JSON format for frontend
        if len(G.nodes()) > 0:
            # Get positions using spring layout
            pos = nx.spring_layout(G, k=2, iterations=50)
            
            # Create a lookup for actual import/function counts from batch results
            file_stats = {}
            for file_result in batch_results['files']:
                if file_result['status'] == 'success':
                    file_path = file_result['file_path']
                    analysis = file_result['analysis']
                    file_stats[file_path] = {
                        'imports': len(analysis.get('imports', [])),
                        'functions': len(analysis.get('definitions', []))
                    }
            
            # Create nodes data
            nodes = []
            for node in G.nodes():
                node_data = G.nodes[node]
                # Get actual counts from batch analysis
                stats = file_stats.get(node, {'imports': 0, 'functions': 0})
                functions_count = stats['functions']
                imports_count = stats['imports']
                
                nodes.append({
                    'id': node,
                    'label': node_data.get('file_name', os.path.basename(node)),
                    'x': float(pos[node][0]),
                    'y': float(pos[node][1]),
                    'size': min(functions_count * 10 + 20, 60),
                    'color': '#4f46e5',
                    'functions': functions_count,
                    'imports': imports_count
                })
            
            # Create edges data
            edges = []
            for source, target in G.edges():
                edges.append({
                    'source': source,
                    'target': target,
                    'x0': float(pos[source][0]),
                    'y0': float(pos[source][1]),
                    'x1': float(pos[target][0]),
                    'y1': float(pos[target][1])
                })
            
            graph_data = {'nodes': nodes, 'edges': edges}
        else:
            graph_data = {'nodes': [], 'edges': []}
        
        socketio.emit('analysis_progress', {
            'stage': 'ai',
            'message': 'AI architecture analysis...'
        })
        
        # AI analysis (optional, can be slow)
        try:
            architecture_analysis = analyze_project_architecture(
                dep_results,
                batch_results,
                project_path
            )
        except Exception as e:
            architecture_analysis = f"AI analysis unavailable: {str(e)}"
        
        # Cache results
        project_id = os.path.basename(project_path)
        analysis_cache[project_id] = {
            'batch': batch_results,
            'dependencies': dep_results,
            'graph': graph_data,
            'architecture': architecture_analysis
        }
        
        socketio.emit('analysis_complete', {
            'project_id': project_id,
            'summary': get_project_summary(batch_results, dep_results)
        })
        
    except Exception as e:
        socketio.emit('analysis_error', {'error': str(e)})


@app.route('/api/projects')
def list_projects():
    """List all analyzed projects"""
    projects = []
    for project_id, data in analysis_cache.items():
        summary = get_project_summary(data['batch'], data['dependencies'])
        projects.append({
            'id': project_id,
            'name': project_id,
            'stats': summary
        })
    return jsonify(projects)


@app.route('/api/project/<project_id>')
def get_project(project_id):
    """Get full analysis for a project"""
    if project_id not in analysis_cache:
        return jsonify({'error': 'Project not found'}), 404
    
    data = analysis_cache[project_id]
    return jsonify({
        'id': project_id,
        'batch': data['batch'],
        'dependencies': data['dependencies'],
        'architecture': data['architecture']
    })


@app.route('/api/project/<project_id>/graph')
def get_project_graph(project_id):
    """Get dependency graph data"""
    if project_id not in analysis_cache:
        return jsonify({'error': 'Project not found'}), 404
    
    return jsonify(analysis_cache[project_id]['graph'])


@app.route('/api/project/<project_id>/file/<path:file_path>')
def get_file_analysis(project_id, file_path):
    """Get analysis for a specific file"""
    if project_id not in analysis_cache:
        return jsonify({'error': 'Project not found'}), 404
    
    batch_data = analysis_cache[project_id]['batch']
    for file_result in batch_data['files']:
        if file_result['file_path'].endswith(file_path):
            return jsonify(file_result)
    
    return jsonify({'error': 'File not found'}), 404


@socketio.on('connect')
def handle_connect():
    """Handle WebSocket connection"""
    emit('connected', {'message': 'Connected to Code Cartographer'})


@socketio.on('disconnect')
def handle_disconnect():
    """Handle WebSocket disconnection"""
    print('Client disconnected')


if __name__ == '__main__':
    print("🚀 Code Cartographer Dashboard starting...")
    print("📊 Open your browser to: http://localhost:5001")
    socketio.run(app, debug=True, host='0.0.0.0', port=5001)

