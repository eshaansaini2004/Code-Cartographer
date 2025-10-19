# Chatbot Testing Guide

## Setup
1. Make sure your `.env` file has a valid `GEMINI_API_KEY`
2. Start the dashboard: `python dashboard/app.py`
3. Open browser to: http://localhost:5001

## Test Cases

### ✅ In-Scope Questions (Should Work)

**Test 1: File-specific question**
```
Q: "What does ai_service.py do?"
Expected: Should explain the functions in ai_service.py (get_ai_summary_sync, analyze_project_architecture)
```

**Test 2: Statistics question**
```
Q: "Which file has the most functions?"
Expected: Should analyze the function counts and identify the file with most functions
```

**Test 3: Dependency question**
```
Q: "Are there any circular dependencies?"
Expected: Should report if circular dependencies exist or confirm none found
```

**Test 4: Hub files question**
```
Q: "What are the hub files in this project?"
Expected: Should list the most imported files
```

**Test 5: Architecture question**
```
Q: "How does the dependency analyzer work?"
Expected: Should explain dependency_analyzer.py based on its functions and structure
```

**Test 6: Import question**
```
Q: "What libraries does the batch_analyzer import?"
Expected: Should list the imports from batch_analyzer.py
```

### ❌ Out-of-Scope Questions (Should Be Rejected)

**Test 7: Weather question**
```
Q: "How's the weather today?"
Expected: "I can only answer questions about the analyzed codebase. Please ask about the files, functions, or architecture in this project."
```

**Test 8: General programming**
```
Q: "How do I implement a binary search tree?"
Expected: Should reject with boundary message
```

**Test 9: Personal question**
```
Q: "What's your name?"
Expected: Should reject with boundary message
```

**Test 10: Unrelated topic**
```
Q: "Tell me about React hooks"
Expected: Should reject with boundary message
```

## Expected Behavior

### ✅ Success Indicators
- Chat section appears after project analysis
- User messages appear on the right (blue background)
- Bot responses appear on the left (purple background with border)
- Loading indicator ("Thinking...") shows while waiting for response
- Responses reference specific files from the analyzed project
- Out-of-scope questions are politely rejected

### ❌ Error Indicators
- Error messages appear in red
- Connection errors handled gracefully
- Missing project_id caught before API call

## Manual Testing Steps

1. **Analyze a project first**
   - Enter project path (e.g., `/Users/eshaansaini/Downloads/code-cartographer-hackathon/services`)
   - Click "Analyze"
   - Wait for analysis to complete
   - Verify chat section appears

2. **Test in-scope questions**
   - Try each question from Test 1-6
   - Verify responses are relevant and reference actual files
   - Check that responses are educational and helpful

3. **Test out-of-scope questions**
   - Try each question from Test 7-10
   - Verify all are rejected with the boundary message
   - Confirm no off-topic responses leak through

4. **Test UI/UX**
   - Verify Enter key sends messages
   - Check scroll behavior (auto-scroll to bottom)
   - Test message styling and animations
   - Verify loading indicator appears/disappears correctly

5. **Test edge cases**
   - Empty messages (should be ignored)
   - Very long questions
   - Rapid-fire questions
   - Special characters in questions

## Automated Test Results

### Test Run 1: [Date/Time]
- [ ] Test 1: ✅/❌
- [ ] Test 2: ✅/❌
- [ ] Test 3: ✅/❌
- [ ] Test 4: ✅/❌
- [ ] Test 5: ✅/❌
- [ ] Test 6: ✅/❌
- [ ] Test 7: ✅/❌
- [ ] Test 8: ✅/❌
- [ ] Test 9: ✅/❌
- [ ] Test 10: ✅/❌

### Notes
- Any unexpected behavior:
- Performance observations:
- UI/UX feedback:

