# 🗺️ Code Cartographer

**AI-Powered Code Analysis Tool for Students & Developers**

> Learn to READ code, not just write it. Understand any codebase in minutes with AI-powered analysis.

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-3.0+-green.svg)](https://flask.palletsprojects.com/)
[![Google Gemini](https://img.shields.io/badge/AI-Google%20Gemini%202.5-orange.svg)](https://ai.google.dev/)

---

## 🎯 What is Code Cartographer?

Students are great at using AI to **write** code (thanks, Copilot!). But when you need to **read and understand** someone else's code - open-source projects, class assignments, internship repos - you're stuck.

**Code Cartographer solves this.** It uses AI to help you:
- 📖 Understand what each file does
- 🕸️ See how files connect (dependency graphs)
- 💬 Ask questions about the codebase in plain English
- 🔍 Find architectural issues and patterns

**No code generation. Just learning.**

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 💬 **AI Chatbot** | Ask "What does ai_service.py do?" - get instant answers (project-scoped only!) |
| 🕸️ **Dependency Graphs** | Interactive visual network showing how files connect |
| 📊 **Real-time Dashboard** | Beautiful web UI with live progress updates |
| ⚡ **Batch Processing** | Analyze 100+ file projects in under 2 minutes |
| 🔍 **Issue Detection** | Find circular dependencies, hub files, orphaned code |
| 🎓 **Educational Focus** | Helps you learn, doesn't do your homework |

---

## 🚀 Getting Started (3 Minutes)

### Step 1: Prerequisites

You need:
- **Python 3.9 or higher** - [Download here](https://www.python.org/downloads/)
- **Git** - [Download here](https://git-scm.com/downloads)
- **Google Gemini API Key** - [Get FREE key here](https://aistudio.google.com/app/apikey)

### Step 2: Clone & Install

```bash
# 1. Clone the repository
git clone https://github.com/eshaansaini2004/Code-Cartographer.git
cd Code-Cartographer

# 2. Create virtual environment
python3 -m venv venv

# 3. Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# 4. Install dependencies (takes 1-2 minutes)
pip install -r requirements.txt
```

### Step 3: Add Your API Key

```bash
# 1. Copy the example environment file
cp .env.example .env

# 2. Edit .env and add your Gemini API key
# Replace YOUR_GEMINI_API_KEY_HERE with your actual key
# Get your FREE key from: https://aistudio.google.com/app/apikey
```

Your `.env` file should look like this:
```
GEMINI_API_KEY=AIzaSyB...your_actual_key_here
```

### Step 4: Run the Dashboard

```bash
# Start the web dashboard
python dashboard/app.py

# You should see:
# 🚀 Code Cartographer Dashboard starting...
# 📊 Open your browser to: http://localhost:5001
```

### Step 5: Analyze a Project

1. **Open your browser** to http://localhost:5001
2. **Enter a project path** (e.g., `/path/to/your/project` or even this repo's `services` folder)
3. **Click "Analyze"** and watch it work! (30-60 seconds)
4. **Explore:**
   - View statistics and dependency graphs
   - Click on nodes to see file details
   - **Use the chatbot!** Ask questions like:
     - "What does ai_service.py do?"
     - "Which file has the most functions?"
     - "Are there any circular dependencies?"

---

## 💡 Example Use Cases

### For Students
- **Learning Open Source**: Clone any GitHub repo and understand it in minutes
- **Class Projects**: Understand starter code before implementing features
- **Code Reviews**: Analyze classmate's code for peer reviews
- **Exam Prep**: Review your own code to understand patterns

### For Developers
- **Onboarding**: Get oriented in new company codebases
- **Legacy Code**: Understand old projects before refactoring
- **Documentation**: Auto-generate architecture insights
- **Pre-Refactor**: Visualize dependencies before making changes

---

## 🛠️ Tech Stack

- **Backend:** Python 3.9+, Flask, Flask-SocketIO
- **AI:** Google Gemini 2.5 Flash (latest model with thinking capabilities)
- **Code Parsing:** tree-sitter (reliable AST parsing)
- **Visualization:** NetworkX + Plotly (interactive graphs)
- **Frontend:** Vanilla JavaScript, HTML5, CSS3
- **VS Code Extension:** TypeScript

---

## 💬 Chatbot Feature

The **killer feature** of Code Cartographer is the AI chatbot that ONLY knows about your analyzed project.

### How It Works
1. Analyze a project in the dashboard
2. Scroll down to the chatbot section
3. Ask questions in plain English
4. Get instant AI-powered answers

### Example Questions
✅ **These work:**
- "What does ai_service.py do?"
- "Which file has the most functions?"
- "Are there any circular dependencies?"
- "How do these files connect?"

❌ **These get rejected:**
- "How's the weather?" → Rejected!
- "Tell me about React" → Rejected!
- "Write me a sorting algorithm" → Rejected!

**Why?** The chatbot is **strictly bounded** to your analyzed codebase. This keeps you focused on learning the code, not getting distracted or getting homework answers.

---

## 🚧 Troubleshooting

### Port 5001 Already in Use
If you see "Address already in use", macOS AirPlay might be using port 5001.

**Solution 1:** Disable AirPlay Receiver
- System Settings → General → AirDrop & Handoff → Turn off "AirPlay Receiver"

**Solution 2:** Use a different port
```python
# Edit dashboard/app.py, change last line to:
socketio.run(app, debug=True, host='0.0.0.0', port=5002)
```

### API Key Not Working
- Make sure you copied the key correctly (no extra spaces)
- Get a new key from https://aistudio.google.com/app/apikey
- Check `.env` file exists and is in the root directory

### Module Not Found Errors
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

---

## 🤝 Contributing

Built for a hackathon, but contributions are welcome!

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

MIT License - Free to use, modify, and distribute.

---

## 🙏 Credits

- **AI:** Google Gemini 2.5 Flash API
- **Parsing:** tree-sitter library
- **Visualization:** Plotly & NetworkX
- **Inspiration:** Students struggling to read code in CS courses

---

## 📧 Contact

**Eshaan Saini** - [GitHub @eshaansaini2004](https://github.com/eshaansaini2004)

Project Link: https://github.com/eshaansaini2004/Code-Cartographer

---

**Made with ❤️ to help students learn to READ code, not just write it.**
