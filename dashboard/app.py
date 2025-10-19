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
            # Get positions using spring layout with better spacing
            pos = nx.spring_layout(G, k=3, iterations=100, scale=2.0, center=(0, 0))
            
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


@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Chat endpoint for project-specific questions
    POST /api/chat
    Body: {"project_id": "services", "message": "What does ai_service.py do?"}
    """
    data = request.json
    project_id = data.get('project_id')
    user_message = data.get('message')
    
    if not project_id or not user_message:
        return jsonify({'error': 'Missing project_id or message'}), 400
    
    if project_id not in analysis_cache:
        return jsonify({'error': 'Project not found. Please analyze a project first.'}), 404
    
    try:
        # Get project context
        project_data = analysis_cache[project_id]
        
        # Build context for AI
        context = build_project_context(project_data)
        
        # Call Gemini with bounded context
        response = ask_gemini_about_project(user_message, context)
        
        return jsonify({'response': response})
        
    except Exception as e:
        return jsonify({'error': f'Chat failed: {str(e)}'}), 500


def build_project_context(project_data):
    """Build a context string from project analysis"""
    batch = project_data['batch']
    deps = project_data['dependencies']
    
    # Build comprehensive context
    context = f"""Project Analysis Summary:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 Statistics:
- Total Files: {batch['statistics']['total_files']}
- Total Functions: {batch['statistics']['total_definitions']}
- Total Imports: {batch['statistics']['total_imports']}
- Total Dependencies: {deps['statistics']['total_dependencies']}

📁 Files in Project:
"""
    
    # Add file details with functions and imports
    for file in batch['files'][:20]:  # Limit to first 20 files to avoid token limits
        if file['status'] == 'success':
            file_path = file['file_path']
            analysis = file['analysis']
            
            context += f"\n{os.path.basename(file_path)}:\n"
            
            # List functions
            if analysis.get('definitions'):
                context += f"  Functions: {', '.join(analysis['definitions'][:10])}\n"
            
            # List imports
            if analysis.get('imports'):
                context += f"  Imports: {', '.join(analysis['imports'][:10])}\n"
    
    # Add dependency information
    if deps.get('circular_dependencies'):
        context += f"\n⚠️ Circular Dependencies: {len(deps['circular_dependencies'])} found\n"
    
    if deps.get('hub_files'):
        context += f"\n🌟 Hub Files (Most Imported):\n"
        for file, count in deps['hub_files'][:5]:
            context += f"  - {os.path.basename(file)} ({count} imports)\n"
    
    if deps.get('orphaned_files'):
        context += f"\n🔌 Orphaned Files: {len(deps['orphaned_files'])} files\n"
    
    return context


def ask_gemini_about_project(question, context):
    """Ask Gemini a question with project context - BOUNDED TO PROJECT ONLY"""
    from google import genai
    
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        return "Error: GEMINI_API_KEY not configured"
    
    client = genai.Client(api_key=api_key)
    
    system_prompt = f"""You are a helpful code analysis assistant for Code Cartographer. 

🎯 YOUR SOLE PURPOSE: Answer questions about the SPECIFIC codebase that has been analyzed below.

📋 PROJECT CONTEXT:
{context}

🚨 CRITICAL RULES:
1. ONLY answer questions about files, functions, dependencies, and structure in THIS specific project
2. If asked about ANYTHING outside this codebase (weather, sports, general programming, other projects, etc.), respond EXACTLY with:
   "I can only answer questions about the analyzed codebase. Please ask about the files, functions, or architecture in this project."
3. Reference specific files and functions from the context above
4. Be concise, educational, and helpful
5. If you don't have enough information from the context, say: "I don't have enough information about that in the analysis. Try analyzing the project again or ask about specific files I can see."
6. Format your responses clearly with bullet points or short paragraphs

EXAMPLES OF VALID QUESTIONS:
- "What does ai_service.py do?"
- "Which file has the most functions?"
- "Are there any circular dependencies?"
- "What are the hub files?"
- "How does the parser_service work?"

EXAMPLES OF INVALID QUESTIONS (respond with the boundary message):
- "How's the weather?"
- "Tell me about React"
- "What's your name?"
- "Help me write a sorting algorithm"
"""
    
    user_prompt = f"User Question: {question}"
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=f"{system_prompt}\n\n{user_prompt}"
        )
        return response.text
    except Exception as e:
        return f"Error communicating with AI: {str(e)}"


if __name__ == '__main__':
    print("🚀 Code Cartographer Dashboard starting...")
    print("📊 Open your browser to: http://localhost:5001")
    socketio.run(app, debug=True, host='0.0.0.0', port=5001)

