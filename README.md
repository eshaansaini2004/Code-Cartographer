# 🗺️ Code Cartographer

**AI-Powered Repository Navigator** - Understand and navigate large codebases with ease using AI-powered analysis, dependency visualization, and interactive dashboards.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.9+-green)
![License](https://img.shields.io/badge/license-MIT-orange)

## ✨ Features

### 🔍 **Single File Analysis**
- AI-powered code summaries using Google Gemini
- Automatic extraction of imports, functions, and calls
- Dependency analysis (what it uses, what uses it)
- Key function identification

### 📦 **Batch Processing**
- Analyze entire projects with progress tracking
- Parallel processing for speed
- Smart caching to avoid re-analysis
- Support for multiple languages (Python, JavaScript, TypeScript)

### 🕸️ **Dependency Visualization**
- Interactive network diagrams
- Visual dependency graphs with Plotly
- Identify hub files (most imported)
- Detect circular dependencies
- Export to HTML, PNG, SVG, JSON

### 🤖 **AI Architecture Analysis**
- Project-level architectural insights
- Pattern detection (MVC, microservices, etc.)
- Entry point identification
- Recommendations for improvements

### 🌐 **Web Dashboard**
- Beautiful, modern UI with dark theme
- Real-time progress tracking via WebSocket
- Interactive dependency graphs
- Project statistics and metrics
- Multiple project support

### 🔌 **VS Code Extension**
- Right-click to analyze files
- Analyze entire workspace
- Visualize dependencies
- Open web dashboard
- Seamless integration

---

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Node.js 18+ (for VS Code extension)
- Google Gemini API key ([Get one free](https://aistudio.google.com/app/apikey))

### Installation

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd "Study pilot"
```

2. **Set up Python environment**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Configure API key**
```bash
echo 'GEMINI_API_KEY="your-api-key-here"' > .env
```

4. **Install VS Code extension** (optional)
```bash
cd vscode-extension
npm install
npm run compile
```

---

## 📖 Usage

### Command Line

#### Analyze a Single File
```bash
python main.py path/to/file.py
```

#### Analyze Entire Project (Batch Mode)
```bash
python main.py --batch path/to/project --exclude "node_modules,venv,__pycache__"
```

#### Generate Dependency Visualization
```bash
python main.py --visualize path/to/project --output graph.html
```

#### Full Analysis with AI Architecture Insights
```bash
python main.py --visualize path/to/project --architecture --output full_analysis.html
```

### Web Dashboard

1. **Start the dashboard**
```bash
python dashboard/app.py
```

2. **Open your browser**
```
http://localhost:5000
```

3. **Analyze projects**
- Enter project path
- Click "Analyze"
- Watch real-time progress
- Explore interactive visualizations

### VS Code Extension

1. **Open the Extension Development Host**
   - Press `F5` in VS Code (with the project open)
   - Or: Run > Start Debugging

2. **Use the commands**
   - **Analyze Current File**: Right-click in editor → "Code Cartographer: Analyze Current File"
   - **Analyze Workspace**: Right-click folder → "Code Cartographer: Analyze Entire Workspace"
   - **Visualize Dependencies**: Command Palette (`Cmd+Shift+P`) → "Code Cartographer: Visualize Dependencies"
   - **Open Dashboard**: Command Palette → "Code Cartographer: Open Dashboard"

---

## 🏗️ Architecture

```
Study pilot/
├── main.py                      # CLI entry point
├── services/                    # Core services
│   ├── parser_service.py        # Code parsing with tree-sitter
│   ├── ai_service.py            # AI analysis with Gemini
│   ├── batch_analyzer.py        # Batch processing
│   ├── dependency_analyzer.py   # Dependency graph building
│   └── visualization_service.py # Graph visualization
├── dashboard/                   # Web dashboard
│   ├── app.py                   # Flask server
│   ├── templates/               # HTML templates
│   └── static/                  # CSS, JavaScript
├── vscode-extension/            # VS Code extension
│   ├── src/extension.ts         # Extension logic
│   └── package.json             # Extension manifest
└── requirements.txt             # Python dependencies
```

---

## 🔧 Configuration

### Environment Variables

Create a `.env` file:

```bash
# Required: Google Gemini API Key
GEMINI_API_KEY="your-api-key-here"

# Optional: Dashboard settings
DASHBOARD_PORT=5000
DASHBOARD_HOST=0.0.0.0
```

### Exclude Patterns

Common patterns to exclude during analysis:

```bash
--exclude "node_modules,venv,__pycache__,.git,dist,build,coverage,.next"
```

---

## 📊 Example Output

### Single File Analysis
```
================================================================================
              CODE CARTOGRAPHER - AI-Powered Repository Navigator               
================================================================================

📄 Analyzing: services/ai_service.py
--------------------------------------------------------------------------------

**Summary:**
This file provides AI-powered code analysis using Google Gemini 2.5 Flash...

**Dependencies (Outbound):**
  • google.genai - For AI-powered code summarization
  • python-dotenv - For loading API keys from environment
  • os - For file system operations

**Key Functions (Inbound):**
  • get_ai_summary_sync() - Generates AI summaries of code files
  • analyze_project_architecture() - Provides architectural insights

✅ Analysis complete!
```

### Batch Analysis
```
📁 Found 47 code files to analyze
Analyzing files: 100%|████████████████████| 47/47 [00:12<00:00, 3.85file/s]

📊 Statistics:
  • Total Files: 47
  • Successfully Analyzed: 47
  • Total Functions: 234
  • Total Dependencies: 156

✅ Batch analysis complete!
```

---

## 🎯 Use Cases

### 1. **Onboarding New Developers**
Help new team members understand the codebase quickly with AI-generated summaries and visual dependency maps.

### 2. **Code Reviews**
Identify architectural issues, circular dependencies, and tightly coupled modules before merging.

### 3. **Refactoring**
Visualize dependencies to safely refactor code and understand the impact of changes.

### 4. **Documentation**
Generate up-to-date architectural documentation automatically.

### 5. **Technical Debt**
Identify hub files, circular dependencies, and orphaned code that needs attention.

---

## 🛠️ Development

### Running Tests
```bash
# Run Python tests
pytest tests/

# Run VS Code extension tests
cd vscode-extension
npm test
```

### Building for Production

#### Package VS Code Extension
```bash
cd vscode-extension
npm install -g vsce
vsce package
# Creates: code-cartographer-0.0.1.vsix
```

#### Deploy Dashboard
```bash
# Using Gunicorn (production)
gunicorn -w 4 -b 0.0.0.0:5000 dashboard.app:app

# Using Docker
docker build -t code-cartographer .
docker run -p 5000:5000 code-cartographer
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙏 Acknowledgments

- **Google Gemini** - AI-powered code analysis
- **tree-sitter** - Fast, reliable code parsing
- **Plotly** - Interactive visualizations
- **Flask** - Web framework
- **VS Code** - Extension platform

---

## 📧 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check the [documentation](./docs/)
- Join our community discussions

---

## 🗺️ Roadmap

- [ ] Support for more languages (Go, Rust, Java, C++)
- [ ] GitHub Actions integration
- [ ] Cloud deployment options
- [ ] Team collaboration features
- [ ] Custom AI model fine-tuning
- [ ] Plugin system for extensibility

---

**Made with ❤️ by developers, for developers**
