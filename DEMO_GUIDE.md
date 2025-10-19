# 🎬 Code Cartographer - Demo Guide & Video Script

## 📋 Pre-Demo Setup (5 minutes before recording)

### Checklist
- [ ] Virtual environment activated: `source venv/bin/activate`
- [ ] `.env` file contains valid `GEMINI_API_KEY`
- [ ] Dashboard server ready: `python dashboard/app.py` (don't start yet)
- [ ] Browser bookmarked to: http://localhost:5001
- [ ] Example project ready: `/Users/eshaansaini/Downloads/code-cartographer-hackathon/services`
- [ ] Screen recording software open (QuickTime/OBS)
- [ ] Terminal window clean and visible
- [ ] Close unnecessary apps/notifications

---

## 🎥 Video Recording Script (5-7 minutes total)

### Scene 1: Introduction (30 seconds)

**[Screen: Terminal/VS Code with project open]**

**Script:**
> "Hi! I'm going to show you Code Cartographer - an AI-powered tool that helps you UNDERSTAND code instead of just writing it.
> 
> As students, we're great at using Copilot to generate code, but when we need to read someone else's code - like an open-source project or class assignment - we're stuck.
>
> Code Cartographer solves this by using AI to explain existing codebases, not write new ones."

**Actions:**
- Show terminal with project directory
- Quick glimpse of some Python files in VS Code

---

### Scene 2: The Problem (30 seconds)

**[Screen: Show a complex codebase with many files]**

**Script:**
> "Look at this project - it has multiple services, dependencies, and architecture patterns. Where do you even start?
>
> You could spend hours reading every file, or you could use Code Cartographer to map it out in minutes."

**Actions:**
- Quickly scroll through project files
- Show services directory with 5-6 Python files
- Display file tree

---

### Scene 3: Dashboard Demo - Analysis (1 minute)

**[Screen: Terminal]**

**Script:**
> "Let's start the dashboard."

**Actions:**
```bash
cd /Users/eshaansaini/Downloads/code-cartographer-hackathon
source venv/bin/activate
python dashboard/app.py
```

**Script (while starting):**
> "It's a Flask web app with WebSocket for real-time updates."

**[Screen: Switch to browser at localhost:5001]**

**Script:**
> "Here's the dashboard. Let me analyze our services directory."

**Actions:**
- Enter project path: `/Users/eshaansaini/Downloads/code-cartographer-hackathon/services`
- Click "Analyze"

**Script (while analyzing):**
> "It's scanning files, building dependency graphs, and running AI analysis. Watch the progress bar - this is real-time via WebSocket."

**Actions:**
- Point to progress bar
- Watch stages: scanning → dependencies → visualization → AI

---

### Scene 4: Dashboard Demo - Results (1.5 minutes)

**[Screen: Browser showing analysis results]**

**Script:**
> "Boom! Check out these results."

**Actions:**
- Scroll to Statistics section

**Script:**
> "We've got 5 files, 25 functions, all analyzed in seconds."

**Actions:**
- Show dependency graph

**Script:**
> "This interactive graph shows how files connect. Bigger nodes have more functions. Hover over one..."

**Actions:**
- Hover over a node to show tooltip with function/import counts

**Script:**
> "See? It shows exactly how many functions and imports each file has."

**Actions:**
- Scroll to Hub Files section

**Script:**
> "These are the 'hub files' - the most imported modules. These are your starting points for understanding the architecture."

**Actions:**
- Scroll to Circular Dependencies

**Script:**
> "And no circular dependencies - that's great! If there were any, this would warn you."

---

### Scene 5: **NEW FEATURE** - Chatbot Demo (2 minutes)

**[Screen: Browser, scroll to Chat section]**

**Script:**
> "Now here's the coolest part - the AI chatbot. But this isn't ChatGPT. This chatbot ONLY knows about the code we just analyzed. Let me show you."

**Actions:**
- Click in chat input field

**Script:**
> "Let's ask: 'What does ai_service.py do?'"

**Actions:**
- Type the question
- Press Enter
- Wait for response

**Script (while waiting):**
> "It's thinking... using Google Gemini to analyze the project context."

**Script (when response appears):**
> "Perfect! It tells me exactly what functions are in ai_service.py and what they do. It's pulling from the actual analysis data."

**Actions:**
- Read the response aloud briefly
- Show another question

**Script:**
> "Let's try: 'Which file has the most functions?'"

**Actions:**
- Type and send
- Show response

**Script:**
> "See? It analyzed the statistics and gave me the answer. But here's the key - watch what happens when I ask something off-topic."

**Actions:**
- Type: "How's the weather today?"
- Send and wait for response

**Script (when response appears):**
> "It refuses! It says it can only answer questions about the analyzed codebase. This keeps you focused on learning the code, not getting distracted."

**Actions:**
- Try one more question: "Are there any circular dependencies?"
- Show response

**Script:**
> "This is powerful for students - you can explore a codebase by asking questions, just like you would with a mentor. But it won't do your homework for you!"

---

### Scene 6: CLI Demo (45 seconds)

**[Screen: Terminal]**

**Script:**
> "You can also use Code Cartographer from the command line. Let me analyze a single file."

**Actions:**
```bash
python main.py services/ai_service.py
```

**Script (while running):**
> "It shows the functions, imports, and AI summary - perfect for quick lookups."

**Actions:**
- Scroll through output
- Point out key sections (Functions, Imports, AI Summary)

---

### Scene 7: VS Code Extension Quick Demo (30 seconds)

**[Screen: VS Code]**

**Script:**
> "And there's even a VS Code extension. Right-click any file..."

**Actions:**
- Right-click a Python file
- Select "Analyze with Code Cartographer"
- Show output in terminal/panel

**Script:**
> "Instant analysis right in your editor. Great for quick references while coding."

---

### Scene 8: Closing (30 seconds)

**[Screen: Back to dashboard or README]**

**Script:**
> "So that's Code Cartographer - a tool that uses AI to help you understand code, not just generate it.
>
> It's perfect for students learning to read codebases, developers joining new projects, or anyone trying to understand open-source code.
>
> The chatbot feature makes it interactive - you can literally have a conversation with your codebase.
>
> It's all on GitHub - link in the description. Thanks for watching!"

**Actions:**
- Quick scroll through README
- Show GitHub link if visible

**[End recording]**

---

## 🎯 Key Talking Points

### Why Code Cartographer?
- Students use Copilot to WRITE code but can't READ code
- Academic integrity: helps learning without doing homework
- Real-world skill: understanding existing codebases

### Unique Features
- **Chatbot with boundaries** - only answers about analyzed code
- **Real-time analysis** - WebSocket progress updates
- **Educational focus** - explains, doesn't generate
- **Interactive graphs** - visual dependency mapping

### Technical Highlights
- Google Gemini 1.5 Flash API
- tree-sitter for static analysis
- NetworkX + Plotly for visualizations
- Flask + WebSocket for real-time updates

---

## 🎬 Recording Tips

### Screen Setup
1. **Resolution:** 1920x1080 (Full HD)
2. **Terminal:** Dark theme, large font (16-18pt)
3. **Browser:** Full screen or maximize
4. **Close:** All unnecessary windows/notifications

### Audio
- Speak clearly and at moderate pace
- Use a decent microphone (AirPods work fine)
- Quiet environment
- Practice once before recording

### Timing
- **Total:** Aim for 5-7 minutes
- Don't rush through chatbot demo (it's the star!)
- Pause for responses to load
- Cut out long waits in editing

### Editing (Optional)
- Speed up slow loading times (1.5x)
- Add text overlays for key points
- Zoom in on important UI elements
- Add background music (low volume)

---

## 🐛 Troubleshooting During Demo

### Dashboard won't start
```bash
# Check port 5001 is free
lsof -i :5001
# Kill if needed
kill -9 <PID>
```

### Gemini API errors
- Check `.env` has valid key
- Try regenerating key at https://aistudio.google.com/app/apikey
- Check internet connection

### Graph not showing
- Reload browser
- Check browser console for errors (F12)
- Re-analyze project if cache is stale

### Chatbot not responding
- Check Gemini API key
- Ensure project is analyzed first
- Check network tab in browser (F12)

---

## 📝 Description Template (for YouTube/submission)

```
🗺️ Code Cartographer - Learn to Read Code with AI

AI-powered code analysis tool that helps students UNDERSTAND existing codebases instead of just generating new code.

✨ Features:
- 💬 Project-scoped AI chatbot (NEW!)
- 🕸️ Interactive dependency graphs
- 📊 Real-time analysis dashboard
- 🔍 Circular dependency detection
- 🎓 Educational focus

🛠️ Built with:
- Python, Flask, tree-sitter
- Google Gemini 1.5 Flash API
- NetworkX, Plotly
- WebSocket for real-time updates

🔗 GitHub: https://github.com/eshaansaini2004/Code-Cartographer

Perfect for:
✅ Students learning to read code
✅ Developers joining new projects
✅ Understanding open-source codebases
✅ Academic learning without compromising integrity

#AI #coding #education #python #webdev #opensource
```

---

## 🎉 Alternative: Quick 2-Minute Demo

If you need a shorter version:

1. **Intro (15s):** Problem statement
2. **Dashboard Analysis (30s):** Analyze project, show progress
3. **Chatbot Demo (60s):** Ask 2-3 questions, show boundary enforcement
4. **Closing (15s):** Call to action

Focus entirely on the chatbot as the killer feature!

---

## 📊 Demo Success Metrics

After recording, verify:
- [ ] All features shown working
- [ ] Chatbot answered correctly (in-scope)
- [ ] Chatbot rejected correctly (out-of-scope)
- [ ] Graphs rendered properly
- [ ] Audio is clear
- [ ] No sensitive info visible (API keys, personal files)
- [ ] GitHub link mentioned
- [ ] Educational value clear

Good luck with your demo! 🚀

