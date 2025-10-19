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
    
    // Show chat section after analysis is complete
    document.getElementById('chatSection').style.display = 'block';
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
        
        // Store project with ID for chat
        currentProject = { ...data, id: projectId };
        
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
        
        // Add edges - make them more visible
        const edgeTraces = graphData.edges.map(edge => ({
            x: [edge.x0, edge.x1, null],  // null creates a break between lines
            y: [edge.y0, edge.y1, null],
            mode: 'lines',
            type: 'scatter',
            line: {
                color: 'rgba(139, 92, 246, 0.4)',  // Purple color, more visible
                width: 2.5
            },
            hoverinfo: 'none',
            showlegend: false
        }));
        
        const layout = {
            title: {
                text: 'Project Dependency Graph',
                font: {
                    size: 20,
                    color: '#f1f5f9'
                }
            },
            showlegend: false,
            hovermode: 'closest',
            plot_bgcolor: '#0f172a',
            paper_bgcolor: '#0f172a',
            font: {
                color: '#f1f5f9',
                size: 12
            },
            xaxis: {
                showgrid: false,
                zeroline: false,
                showticklabels: false,
                range: [-2.5, 2.5]  // Center the graph
            },
            yaxis: {
                showgrid: false,
                zeroline: false,
                showticklabels: false,
                range: [-2.5, 2.5]  // Center the graph
            },
            margin: {
                l: 40,
                r: 40,
                t: 60,
                b: 40
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

// ============================================
// CHAT FUNCTIONALITY
// ============================================

// Send chat message
async function sendMessage() {
    const input = document.getElementById('chatInput');
    const message = input.value.trim();
    
    if (!message) {
        return;
    }
    
    if (!currentProject) {
        showError('Please analyze a project first');
        return;
    }
    
    // Add user message to UI
    addChatMessage(message, 'user');
    input.value = '';
    
    // Show loading indicator
    const loadingId = addChatLoading();
    
    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                project_id: currentProject.id,
                message: message
            })
        });
        
        const data = await response.json();
        
        // Remove loading indicator
        removeChatLoading(loadingId);
        
        if (!response.ok) {
            addChatMessage(data.error || 'Failed to get response', 'error');
            return;
        }
        
        // Add bot response to UI
        addChatMessage(data.response, 'bot');
        
    } catch (error) {
        removeChatLoading(loadingId);
        addChatMessage('Error: Could not connect to chat service', 'error');
    }
}

// Add chat message to UI
function addChatMessage(text, type) {
    const container = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `chat-message ${type}`;
    messageDiv.textContent = text;
    container.appendChild(messageDiv);
    
    // Scroll to bottom
    container.scrollTop = container.scrollHeight;
}

// Add loading indicator
function addChatLoading() {
    const container = document.getElementById('chatMessages');
    const loadingDiv = document.createElement('div');
    const loadingId = 'loading-' + Date.now();
    loadingDiv.id = loadingId;
    loadingDiv.className = 'chat-loading';
    loadingDiv.textContent = 'Thinking';
    container.appendChild(loadingDiv);
    
    // Scroll to bottom
    container.scrollTop = container.scrollHeight;
    
    return loadingId;
}

// Remove loading indicator
function removeChatLoading(loadingId) {
    const loadingDiv = document.getElementById(loadingId);
    if (loadingDiv) {
        loadingDiv.remove();
    }
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
    
    // Allow Enter key to send chat message
    const chatInput = document.getElementById('chatInput');
    if (chatInput) {
        chatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
    }
});

