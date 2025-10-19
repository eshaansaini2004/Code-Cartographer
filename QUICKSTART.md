# 🚀 Quick Start Guide - Code Cartographer

Get up and running in 5 minutes!

## Step 1: Setup (2 minutes)

```bash
# 1. Activate virtual environment
cd "/Users/eshaansaini/Downloads/Study pilot"
source venv/bin/activate

# 2. Verify installation
python main.py --help
```

## Step 2: Test Single File Analysis (1 minute)

```bash
# Analyze the test example file
python main.py test_example.py
```

**Expected output:** AI-powered summary with dependencies and key functions.

## Step 3: Test Batch Analysis (1 minute)

```bash
# Analyze the services directory
python main.py --batch services --exclude "__pycache__"
```

**Expected output:** Statistics for all 5 service files.

## Step 4: Generate Visualization (1 minute)

```bash
# Create dependency graph
python main.py --visualize services --architecture --output my_graph.html
```

**Expected output:** 
- `my_graph.html` - Interactive graph
- `my_graph_stats.html` - Statistics
- `my_graph_architecture.txt` - AI analysis

Open `my_graph.html` in your browser to see the interactive visualization!

## Step 5: Launch Web Dashboard (30 seconds)

```bash
# Start the dashboard
python dashboard/app.py
```

Then open: **http://localhost:5000**

### Try it out:
1. Enter a project path (e.g., `/Users/eshaansaini/Downloads/Study pilot/services`)
2. Click "Analyze"
3. Watch real-time progress
4. Explore the interactive visualizations!

---

## Using VS Code Extension

### Option 1: Extension Development Host

1. Open this project in VS Code
2. Press `F5` to launch Extension Development Host
3. In the new window, try these commands:

**Analyze Current File:**
- Right-click in any Python/JS/TS file
- Select "Code Cartographer: Analyze Current File"

**Analyze Workspace:**
- Open Command Palette (`Cmd+Shift+P` or `Ctrl+Shift+P`)
- Type "Code Cartographer: Analyze Entire Workspace"

**Visualize Dependencies:**
- Command Palette → "Code Cartographer: Visualize Dependencies"
- Opens HTML graph in your browser

**Open Dashboard:**
- Command Palette → "Code Cartographer: Open Dashboard"
- Launches web dashboard at http://localhost:5000

---

## Common Commands Cheat Sheet

```bash
# Single file
python main.py <file_path>

# Batch with exclusions
python main.py --batch <directory> --exclude "node_modules,venv"

# Visualization with AI
python main.py --visualize <directory> --architecture --output graph.html

# Web dashboard
python dashboard/app.py

# VS Code extension (from vscode-extension/)
npm run compile
```

---

## Troubleshooting

### "Module not found" error
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### "API key not valid" error
```bash
# Make sure .env file has your Gemini API key
echo 'GEMINI_API_KEY="your-actual-key"' > .env
```

### VS Code extension not showing
1. Make sure you're in Extension Development Host (F5)
2. Check Output panel for errors
3. Recompile: `cd vscode-extension && npm run compile`

### Dashboard won't start
```bash
# Install Flask dependencies
pip install flask flask-cors flask-socketio
```

---

## Next Steps

- Read the full [README.md](./README.md) for detailed documentation
- Explore the [services/](./services/) directory to understand the architecture
- Try analyzing your own projects!
- Customize the `.gitignore` patterns for your needs

---

## Need Help?

- Check the [README.md](./README.md) for detailed docs
- Look at example outputs in the project
- Review the code in `services/` for implementation details

**Happy Cartographing! 🗺️**

