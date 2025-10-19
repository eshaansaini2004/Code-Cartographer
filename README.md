# 🗺️ Code Cartographer

**AI-Powered Code Analysis Tool for Learning**

> Helping students understand code, not just generate it.

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-3.0+-green.svg)](https://flask.palletsprojects.com/)
[![Google Gemini](https://img.shields.io/badge/AI-Google%20Gemini-orange.svg)](https://ai.google.dev/)

## 🎯 The Problem

Students rely on tools like Copilot to write code without understanding it. When they encounter existing codebases - whether open-source projects, class assignments, or internship code - they're lost. 

**Code Cartographer uses AI differently:** to help you UNDERSTAND code that already exists, not write it for you.

## ✨ Features

- 🤖 **AI Explanations** - Google Gemini explains code in plain English
- 🕸️ **Dependency Graphs** - Interactive visualizations of how files connect
- 📊 **Real-time Dashboard** - Beautiful web UI with live progress updates
- ⚡ **Batch Processing** - Analyze entire projects in seconds with caching
- 🔍 **Issue Detection** - Find circular dependencies and architectural problems
- 🎓 **Educational Focus** - Learn to read and understand code, not just generate it

## 🚀 Quick Start

```bash
# Clone the repo
git clone https://github.com/eshaansaini2004/Code-Cartographer.git
cd Code-Cartographer

# Set up virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Add your Gemini API key
cp .env.example .env
# Edit .env and add your API key from: https://aistudio.google.com/app/apikey

# Start the dashboard
python dashboard/app.py

# Open http://localhost:5001
```

## 📖 Usage Examples

### Analyze a Single File
```bash
python main.py path/to/file.py
```

### Analyze Entire Project
```bash
python main.py --batch path/to/project --exclude "node_modules,venv"
```

### Generate Dependency Visualization
```bash
python main.py --visualize path/to/project --architecture --output graph.html
```

### Web Dashboard (Recommended!)
```bash
python dashboard/app.py
# Open http://localhost:5001
# Enter project path and click "Analyze"
```

## 🛠️ Tech Stack

- **Backend:** Python 3.9+, Flask, tree-sitter
- **AI:** Google Gemini 2.5 Flash API
- **Visualization:** NetworkX, Plotly
- **Frontend:** HTML/CSS/JavaScript with WebSocket
- **Extension:** TypeScript for VS Code

## 📸 Screenshots

### Dashboard Home
![Dashboard](screenshots/dashboard.png)

### Interactive Dependency Graph
![Graph](screenshots/graph.png)

### AI Architecture Analysis
![Analysis](screenshots/analysis.png)

## 🎓 Educational Philosophy

Code Cartographer promotes **active learning** over passive code generation:

- ✅ Teaches code reading skills
- ✅ Helps understand architectural patterns
- ✅ Encourages exploration of real codebases
- ✅ Uses AI to explain, not replace thinking

## 🎯 Use Cases

- **Onboarding** - Quickly understand new projects
- **Learning** - Explore open-source codebases
- **Code Review** - Identify architectural issues
- **Refactoring** - Visualize dependencies before changes
- **Documentation** - Auto-generate architecture docs

## 📚 Documentation

- [Quick Start Guide](QUICKSTART.md) - Get up and running in 5 minutes
- [Setup Guide](SETUP_GUIDE.md) - Detailed installation instructions
- [Project Summary](PROJECT_SUMMARY.md) - Complete feature overview
- [Test Results](TEST_RESULTS.md) - Comprehensive testing documentation

## 🤝 Contributing

This project was built for educational purposes. Contributions welcome!

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

MIT License - See LICENSE file for details

## 🙏 Acknowledgments

- Built with [Google Gemini API](https://ai.google.dev/) for AI-powered code analysis
- Uses [tree-sitter](https://tree-sitter.github.io/) for reliable code parsing
- Visualizations powered by [Plotly](https://plotly.com/) and [NetworkX](https://networkx.org/)

## 📧 Contact

Eshaan Saini - [@eshaansaini2004](https://github.com/eshaansaini2004)

Project Link: [https://github.com/eshaansaini2004/Code-Cartographer](https://github.com/eshaansaini2004/Code-Cartographer)

---

**Made with ❤️ for students who want to truly understand code**
