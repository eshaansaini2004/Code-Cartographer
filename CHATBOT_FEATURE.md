# 💬 Chatbot Feature Documentation

## Overview

The Code Cartographer Chatbot is an AI-powered assistant that helps you understand your analyzed codebase through natural language questions. Unlike general-purpose AI chatbots, this one is **strictly bounded** to only answer questions about the specific project you've analyzed.

## Key Features

### 🎯 Project-Scoped Responses
- Only answers questions about the analyzed codebase
- Rejects off-topic questions politely
- Uses actual analysis data (files, functions, dependencies)
- References specific files and functions from your project

### 🧠 Powered by Google Gemini
- Uses Gemini 1.5 Flash for fast, accurate responses
- Context-aware: knows your project structure
- Educational tone: explains concepts clearly
- Concise and helpful answers

### 🔒 Smart Boundaries
The chatbot will **refuse** to answer:
- General programming questions
- Questions about other projects
- Personal questions
- Off-topic subjects (weather, sports, etc.)

Instead, it will respond:
> "I can only answer questions about the analyzed codebase. Please ask about the files, functions, or architecture in this project."

## How It Works

### 1. Analysis Phase
When you analyze a project, the system:
- Extracts all functions, imports, and dependencies
- Builds a dependency graph
- Stores analysis results in memory cache
- Prepares context for the chatbot

### 2. Context Building
For each chat request, the system creates a context containing:
- Project statistics (files, functions, imports, dependencies)
- List of files with their functions and imports (up to 20 files)
- Circular dependencies (if any)
- Hub files (most imported)
- Orphaned files

### 3. AI Processing
- User question + project context sent to Gemini
- System prompt enforces boundaries
- AI generates response based ONLY on provided context
- Response returned to user interface

## Usage Examples

### ✅ Valid Questions

**File-specific:**
```
Q: "What does ai_service.py do?"
A: "ai_service.py contains 2 main functions for AI-powered analysis:
   - get_ai_summary_sync(): Generates code summaries using Google Gemini
   - analyze_project_architecture(): Analyzes overall project structure
   It imports google.genai and python-dotenv for API integration."
```

**Statistics:**
```
Q: "Which file has the most functions?"
A: "dependency_analyzer.py has the most functions with 8 total, including:
   - analyze_dependencies()
   - get_dependency_summary()
   - _build_graph()
   [...]"
```

**Architecture:**
```
Q: "Are there any circular dependencies?"
A: "No circular dependencies were detected in this project. This is good!
   It means your files have a clean, acyclic dependency structure."
```

**Dependencies:**
```
Q: "What are the hub files?"
A: "The hub files (most imported) are:
   - parser_service.py (5 imports)
   - batch_analyzer.py (3 imports)
   These are core utilities used throughout the project."
```

### ❌ Invalid Questions (Will Be Rejected)

```
Q: "How's the weather?"
A: "I can only answer questions about the analyzed codebase..."

Q: "Tell me about React hooks"
A: "I can only answer questions about the analyzed codebase..."

Q: "What's your name?"
A: "I can only answer questions about the analyzed codebase..."
```

## API Endpoint

### POST `/api/chat`

**Request:**
```json
{
  "project_id": "my-project",
  "message": "What does ai_service.py do?"
}
```

**Response (Success):**
```json
{
  "response": "ai_service.py contains 2 main functions..."
}
```

**Response (Error):**
```json
{
  "error": "Project not found. Please analyze a project first."
}
```

## UI Components

### Chat Section
- Appears after project analysis completes
- Clean, modern chat interface
- User messages: right-aligned, blue background
- Bot messages: left-aligned, purple background with border
- Error messages: left-aligned, red background

### Input Field
- Text input with placeholder: "Ask about functions, dependencies, architecture..."
- Send button
- Enter key support for quick messaging

### Loading Indicator
- Animated "Thinking..." indicator while waiting for response
- Automatically removed when response arrives

## Technical Implementation

### Backend (`dashboard/app.py`)

**Chat Endpoint:**
```python
@app.route('/api/chat', methods=['POST'])
def chat():
    # Validate project_id and message
    # Get project context from analysis_cache
    # Build context string
    # Call Gemini with bounded system prompt
    # Return response
```

**Context Builder:**
```python
def build_project_context(project_data):
    # Extract statistics
    # List files with functions/imports
    # Add dependency information
    # Return formatted context string
```

**AI Integration:**
```python
def ask_gemini_about_project(question, context):
    # Configure Gemini client
    # Create system prompt with boundaries
    # Send question + context to Gemini
    # Return response
```

### Frontend (`dashboard/static/js/app.js`)

**Send Message:**
```javascript
async function sendMessage() {
    // Validate input
    // Add user message to UI
    // Show loading indicator
    // POST to /api/chat
    // Display bot response
    // Handle errors
}
```

**Message Display:**
```javascript
function addChatMessage(text, type) {
    // Create message div
    // Apply styling based on type (user/bot/error)
    // Add to chat container
    // Auto-scroll to bottom
}
```

## Benefits

### For Students
- ✅ **Learn by Asking:** Explore codebases through natural conversation
- ✅ **Stay Focused:** Boundaries prevent distraction from off-topic questions
- ✅ **Instant Feedback:** Get immediate answers about code structure
- ✅ **Safe Learning:** Can't accidentally get help writing code (violating academic integrity)

### For Developers
- ✅ **Quick Understanding:** Get oriented in new codebases fast
- ✅ **Documentation Gap:** Ask questions when documentation is missing
- ✅ **Architecture Insights:** Understand high-level patterns quickly
- ✅ **Dependency Navigation:** Find relationships between files

## Security & Privacy

- ✅ **No Code Storage:** Analysis cached in memory only (lost on restart)
- ✅ **API Key Security:** Gemini API key stored in `.env` (gitignored)
- ✅ **Local Processing:** All analysis runs on your machine
- ✅ **Bounded Context:** Only analyzed project data sent to Gemini API

## Future Enhancements

Potential improvements for future versions:
- 🔮 Persistent chat history across sessions
- 🔮 Export chat conversations for notes
- 🔮 Multi-turn conversations with context memory
- 🔮 Code snippet highlighting in responses
- 🔮 Follow-up question suggestions
- 🔮 Voice input/output support
- 🔮 Integration with VS Code extension

## Troubleshooting

### Chatbot not appearing
- **Cause:** Project not analyzed yet
- **Solution:** Analyze a project first, then chat section will appear

### "Project not found" error
- **Cause:** Analysis cache cleared or server restarted
- **Solution:** Re-analyze the project

### Slow responses
- **Cause:** Large project context or Gemini API latency
- **Solution:** Normal for first few requests; subsequent requests should be faster

### API key errors
- **Cause:** Missing or invalid GEMINI_API_KEY
- **Solution:** Check `.env` file, get key from https://aistudio.google.com/app/apikey

## Example Use Case

**Scenario:** Student joins an open-source project for class

1. Clone the project repository
2. Open Code Cartographer dashboard
3. Analyze the project
4. Ask chatbot:
   - "What's the main entry point of this application?"
   - "What does the authentication service do?"
   - "How do the frontend and backend communicate?"
   - "Which files handle database operations?"
5. Read the relevant files mentioned in responses
6. Ask follow-up questions about specific functions
7. Build mental map of the codebase

**Result:** Student understands the project architecture without reading every single file.

## Credits

- **AI:** Google Gemini 1.5 Flash API
- **UI Inspiration:** Modern chat interfaces (Discord, Slack)
- **Educational Philosophy:** Active learning through questioning

