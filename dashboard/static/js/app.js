// Code Cartographer Dashboard JavaScript

// WebSocket connection
const socket = io();

let currentProject = null;

// Socket event handlers
socket.on('connect', () => {
    console.log('Connected to server');
});

socket.on('analysis_progress', (data) => {
    updateProgress(data);
});

socket.on('analysis_complete', (data) => {
    hideProgress();
    loadProject(data.project_id);
    loadProjectsList();
    showSuccess('Analysis complete!');
});

socket.on('analysis_error', (data) => {
    hideProgress();
    showError(`Analysis failed: ${data.error}`);
});

// Analyze project
async function analyzeProject() {
    const projectPath = document.getElementById('projectPath').value.trim();
    
    if (!projectPath) {
        showError('Please enter a project path');
        return;
    }
    
    showProgress();
    
    try {
        const response = await fetch('/api/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                path: projectPath,
                exclude: ['node_modules', 'venv', '__pycache__', '.git', 'dist', 'build']
            })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Analysis failed');
        }
        
    } catch (error) {
        hideProgress();
        showError(error.message);
    }
}

// Load projects list
async function loadProjectsList() {
    try {
        const response = await fetch('/api/projects');
        const projects = await response.json();
        
        const container = document.getElementById('projectsList');
        
        if (projects.length === 0) {
            container.innerHTML = '<p class="empty-state">No projects analyzed yet. Analyze a project to get started!</p>';
            return;
        }
        
        container.innerHTML = projects.map(project => `
            <div class="project-item" onclick="loadProject('${project.id}')">
                <div class="project-name">📁 ${project.name}</div>
                <div class="project-stats">
                    <div class="stat-item">
                        <span class="stat-label">Files</span>
                        <span class="stat-value">${project.stats.total_files || 0}</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-label">Functions</span>
                        <span class="stat-value">${project.stats.total_definitions || 0}</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-label">Dependencies</span>
                        <span class="stat-value">${project.stats.total_dependencies || 0}</span>
                    </div>
                </div>
            </div>
        `).join('');
        
    } catch (error) {
        console.error('Failed to load projects:', error);
    }
}

// Load project details
async function loadProject(projectId) {
    try {
        const response = await fetch(`/api/project/${projectId}`);
        const data = await response.json();
        
        currentProject = data;
        
        // Show project details section
        document.getElementById('projectDetails').style.display = 'block';
        
        // Display statistics
        displayStats(data.batch.statistics);
        
        // Display dependency graph
        displayGraph(projectId);
        
        // Display architecture analysis
        displayArchitecture(data.architecture);
        
        // Display hub files
        displayHubFiles(data.dependencies.hub_files);
        
        // Display circular dependencies
        displayCircularDeps(data.dependencies.circular_dependencies);
        
        // Scroll to details
        document.getElementById('projectDetails').scrollIntoView({ behavior: 'smooth' });
        
    } catch (error) {
        showError(`Failed to load project: ${error.message}`);
    }
}

// Display statistics
function displayStats(stats) {
    const container = document.getElementById('statsContainer');
    
    const statsData = [
        { label: 'Total Files', value: stats.total_files, icon: '📄' },
        { label: 'Functions', value: stats.total_definitions, icon: '⚡' },
        { label: 'Imports', value: stats.total_imports, icon: '📦' },
        { label: 'Function Calls', value: stats.total_calls, icon: '🔗' }
    ];
    
    container.innerHTML = statsData.map(stat => `
        <div class="stat-card">
            <div class="stat-label">${stat.icon} ${stat.label}</div>
            <div class="stat-value">${stat.value}</div>
        </div>
    `).join('');
}

// Display dependency graph
async function displayGraph(projectId) {
    try {
        const response = await fetch(`/api/project/${projectId}/graph`);
        const graphData = await response.json();
        
        if (!graphData || !graphData.nodes || graphData.nodes.length === 0) {
            document.getElementById('graphContainer').innerHTML = 
                '<p class="empty-state">No dependencies found in this project</p>';
            return;
        }
        
        // Create Plotly graph
        const trace = {
            x: graphData.nodes.map(n => n.x),
            y: graphData.nodes.map(n => n.y),
            mode: 'markers+text',
            type: 'scatter',
            text: graphData.nodes.map(n => n.label),
            textposition: 'top center',
            marker: {
                size: graphData.nodes.map(n => n.size),
                color: graphData.nodes.map(n => n.color),
                line: {
                    color: 'white',
                    width: 2
                }
            },
            hoverinfo: 'text',
            hovertext: graphData.nodes.map(n => 
                `${n.label}<br>Functions: ${n.functions}<br>Imports: ${n.imports}`
            )
        };
        
        // Add edges
        const edgeTraces = graphData.edges.map(edge => ({
            x: [edge.x0, edge.x1],
            y: [edge.y0, edge.y1],
            mode: 'lines',
            type: 'scatter',
            line: {
                color: 'rgba(100, 116, 139, 0.3)',
                width: 2
            },
            hoverinfo: 'none'
        }));
        
        const layout = {
            title: 'Project Dependency Graph',
            showlegend: false,
            hovermode: 'closest',
            plot_bgcolor: '#0f172a',
            paper_bgcolor: '#0f172a',
            font: {
                color: '#f1f5f9'
            },
            xaxis: {
                showgrid: false,
                zeroline: false,
                showticklabels: false
            },
            yaxis: {
                showgrid: false,
                zeroline: false,
                showticklabels: false
            }
        };
        
        Plotly.newPlot('graphContainer', [...edgeTraces, trace], layout, {
            responsive: true
        });
        
    } catch (error) {
        console.error('Failed to load graph:', error);
        document.getElementById('graphContainer').innerHTML = 
            '<p class="error-message">Failed to load dependency graph</p>';
    }
}

// Display architecture analysis
function displayArchitecture(architecture) {
    const container = document.getElementById('architectureContainer');
    container.textContent = architecture || 'No architecture analysis available';
}

// Display hub files
function displayHubFiles(hubFiles) {
    const container = document.getElementById('hubFilesContainer');
    
    if (!hubFiles || hubFiles.length === 0) {
        container.innerHTML = '<p class="empty-state">No hub files detected</p>';
        return;
    }
    
    container.innerHTML = hubFiles.slice(0, 10).map(([file, count]) => `
        <div class="file-item">
            <span class="file-name">${getFileName(file)}</span>
            <span class="file-badge">${count} imports</span>
        </div>
    `).join('');
}

// Display circular dependencies
function displayCircularDeps(circularDeps) {
    const container = document.getElementById('circularDepsContainer');
    
    if (!circularDeps || circularDeps.length === 0) {
        container.innerHTML = '<p class="success-message">✅ No circular dependencies detected!</p>';
        return;
    }
    
    container.innerHTML = circularDeps.map(cycle => `
        <div class="circular-item">
            ${cycle.map(getFileName).join(' → ')}
        </div>
    `).join('');
}

// Helper functions
function getFileName(path) {
    return path.split('/').pop();
}

function showProgress() {
    document.getElementById('progressContainer').style.display = 'block';
    document.getElementById('progressBar').style.width = '10%';
}

function updateProgress(data) {
    const stages = {
        'scanning': 25,
        'dependencies': 50,
        'visualization': 75,
        'ai': 90
    };
    
    const progress = stages[data.stage] || 10;
    document.getElementById('progressBar').style.width = `${progress}%`;
    document.getElementById('progressMessage').textContent = data.message;
}

function hideProgress() {
    setTimeout(() => {
        document.getElementById('progressContainer').style.display = 'none';
        document.getElementById('progressBar').style.width = '0%';
    }, 1000);
}

function showSuccess(message) {
    // You can implement a toast notification here
    console.log('Success:', message);
}

function showError(message) {
    alert(`Error: ${message}`);
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadProjectsList();
    
    // Allow Enter key to trigger analysis
    document.getElementById('projectPath').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            analyzeProject();
        }
    });
});

