# 🗺️ Code Cartographer - Complete Setup Guide

Welcome to Code Cartographer! This guide will walk you through the complete setup process.

---

## 📋 Prerequisites

- **Python 3.9+** installed on your system
- **Node.js 18+** and npm
- **VS Code** (for the extension)
- **OpenAI API Key** (get one at https://platform.openai.com/api-keys)

---

## 🚀 Quick Start

### Step 1: Set Up Python Environment

The Python virtual environment and dependencies are **already installed**! ✅

But if you need to reinstall:

```bash
# Navigate to project directory
cd "/Users/eshaansaini/Downloads/Study pilot"

# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Configure Your OpenAI API Key

**IMPORTANT:** You need to create a `.env` file with your OpenAI API key.

1. Get your API key from: https://platform.openai.com/api-keys

2. Create a `.env` file in the project root:
   ```bash
   cd "/Users/eshaansaini/Downloads/Study pilot"
   touch .env
   ```

3. Open the `.env` file and add:
   ```
   OPENAI_API_KEY="sk-your-actual-key-here"
   ```

   Replace `sk-your-actual-key-here` with your real API key!

### Step 3: Test the Command-Line Tool

Let's test that everything works:

```bash
# Make sure you're in the project root and venv is activated
cd "/Users/eshaansaini/Downloads/Study pilot"
source venv/bin/activate

# Analyze one of the project files
python main.py services/parser_service.py
```

You should see:
1. A nice header
2. Progress messages for 3 steps
3. An AI-generated analysis with Summary, Dependencies, and Key Functions

If you see this, **the core system is working!** 🎉

### Step 4: Set Up the VS Code Extension

The extension files are **already created**! ✅

But let's make sure it's compiled:

```bash
cd "/Users/eshaansaini/Downloads/Study pilot/vscode-extension"
npm install  # Already done, but good to verify
npm run compile
```

### Step 5: Run the Extension

1. **Open VS Code**

2. **Open the Project Folder:**
   - File → Open Folder
   - Select: `/Users/eshaansaini/Downloads/Study pilot`
   - ⚠️ **Important:** Open the main project folder, NOT the vscode-extension subfolder

3. **Navigate to the Extension:**
   - In the Explorer sidebar, go to `vscode-extension/`
   - Right-click on the `vscode-extension` folder
   - Select "Open in Integrated Terminal" (optional)

4. **Launch Extension Development Host:**
   - Press `F5` (or Run → Start Debugging)
   - This will open a new VS Code window with "[Extension Development Host]" in the title

5. **Test the Extension:**
   - In the Extension Development Host window, open any Python/JS/TS file
   - Or create a test file (see example below)
   - Right-click anywhere in the code editor
   - Select **"Analyze with Code Cartographer"**
   - Wait 10-30 seconds for the AI analysis
   - A new tab will open with the full analysis!

---

## 🧪 Testing with a Sample File

Create a test file to analyze:

```bash
cd "/Users/eshaansaini/Downloads/Study pilot"
```

Then create `test_example.py`:

```python
# test_example.py
import os
import json
from typing import List, Dict

def load_config(file_path: str) -> Dict:
    """Load configuration from a JSON file."""
    with open(file_path, 'r') as f:
        return json.load(f)

def process_data(data: List[int]) -> int:
    """Process a list of integers and return the sum."""
    return sum(data)

def main():
    config = load_config('config.json')
    result = process_data([1, 2, 3, 4, 5])
    print(f"Result: {result}")

if __name__ == "__main__":
    main()
```

Now test it:

**Command Line:**
```bash
python main.py test_example.py
```

**VS Code Extension:**
1. Open `test_example.py` in the Extension Development Host
2. Right-click → "Analyze with Code Cartographer"

---

## 🔍 How It Works

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     VS Code Extension                       │
│                    (TypeScript/Node.js)                     │
│                                                             │
│  • Right-click context menu                                │
│  • Executes Python script                                  │
│  • Displays results in new tab                             │
└─────────────────┬───────────────────────────────────────────┘
                  │ Calls via child_process
                  ▼
┌─────────────────────────────────────────────────────────────┐
│                  main.py (Orchestrator)                     │
└─────────────────┬───────────────────────────────────────────┘
                  │
        ┌─────────┴─────────┐
        ▼                   ▼
┌─────────────────┐   ┌─────────────────┐
│ parser_service  │   │  ai_service     │
│  (tree-sitter)  │   │   (OpenAI)      │
│                 │   │                 │
│ • Parse AST     │   │ • Generate      │
│ • Extract       │   │   summary       │
│   imports       │   │ • Explain       │
│ • Find funcs    │   │   connections   │
└─────────────────┘   └─────────────────┘
```

### The Magic: Hybrid Approach

1. **tree-sitter** (deterministic) extracts FACTS:
   - What modules are imported
   - What functions are defined
   - What functions are called

2. **GPT-4** (AI) provides UNDERSTANDING:
   - Why does this file exist?
   - How do these pieces connect?
   - What role does it play in the codebase?

This combination is more reliable than pure AI guessing!

---

## 🛠️ Troubleshooting

### "OpenAI API key not found"
- Make sure you created a `.env` file in the project root
- Check that it contains: `OPENAI_API_KEY="your-key"`
- Don't use the placeholder text - use your real key!

### "main.py not found"
- Open the entire project folder in VS Code, not just the extension folder
- The workspace root should be `/Users/eshaansaini/Downloads/Study pilot`

### "Unsupported file extension"
- Currently supports: `.py`, `.js`, `.ts`, `.jsx`, `.tsx`
- Other languages can be added by updating `parser_service.py`

### Extension doesn't appear in the right-click menu
- Make sure you compiled the extension: `npm run compile`
- Try reloading the Extension Development Host: Cmd+R

### Tree-sitter parsing errors
- tree-sitter is very robust, but sometimes complex syntax causes issues
- The tool will show warnings but continue with partial results

---

## 📊 What You Get

The analysis includes:

1. **Summary:** High-level explanation of the file's purpose
2. **Dependencies (Outbound):** What this file uses
3. **Key Functions (Inbound):** What this file provides to others
4. **Insights:** Patterns, potential issues, or architectural notes

---

## 🎯 Next Steps

Now that you have the MVP working:

1. **Test it on real codebases:** Try it on large, unfamiliar repositories
2. **Improve the queries:** Tune the tree-sitter patterns for better extraction
3. **Add more languages:** Go, Java, C++, etc.
4. **Visualize connections:** Create a graph view of file dependencies
5. **Cache results:** Speed up repeated analyses
6. **Add configuration:** Let users customize the AI prompt

---

## 📝 Project Structure

```
Study pilot/
├── main.py                      # Main orchestrator
├── services/
│   ├── parser_service.py       # tree-sitter integration
│   └── ai_service.py           # OpenAI integration
├── requirements.txt            # Python dependencies
├── .env                        # API keys (create this!)
├── .gitignore                 # Git ignore rules
├── README.md                  # Project overview
├── SETUP_GUIDE.md            # This file
├── venv/                     # Python virtual environment
└── vscode-extension/         # VS Code extension
    ├── src/
    │   └── extension.ts      # Extension logic
    ├── package.json          # Extension manifest
    ├── tsconfig.json         # TypeScript config
    └── out/                  # Compiled JavaScript
```

---

## 🎓 Learning Resources

- **tree-sitter:** https://tree-sitter.github.io/tree-sitter/
- **VS Code Extension API:** https://code.visualstudio.com/api
- **OpenAI API:** https://platform.openai.com/docs

---

## ✅ Checklist

- [ ] Python virtual environment created and activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] `.env` file created with OpenAI API key
- [ ] Command-line tool tested (`python main.py <file>`)
- [ ] VS Code extension compiled (`npm run compile`)
- [ ] Extension tested in Extension Development Host (F5)
- [ ] Successfully analyzed a file via right-click menu

---

**You're all set! Happy code exploring! 🗺️🧭**



