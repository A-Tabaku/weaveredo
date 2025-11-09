# 🚀 HOW TO TEST THE COMPLETE SYSTEM

## Quick Start (2 Steps)

### Step 1: Start the API Server
Open a terminal and run:
```bash
cd /Users/iceca/Documents/Weave/backend
uvicorn api.server:app --port 8000
```

Keep this terminal open! The server must stay running.

### Step 2: Run the Complete Flow Test
Open a **NEW** terminal (keep the first one open!) and run:
```bash
cd /Users/iceca/Documents/Weave/backend
python test_complete_flow.py
```

---

## What Happens

**The test runs the full pipeline:**

1. **Entry Agent** (Interactive)
   - You'll answer questions about your character
   - Agent builds a character concept
   - Outputs JSON

2. **Character Development** (Automatic)
   - 7 AI agents analyze the character
   - Each creates a checkpoint
   - You approve or reject each one

3. **Final Profile** (Complete)
   - All character data combined
   - Images generated
   - Saved as JSON file

---

## Example Commands

### Full Interactive Mode (Recommended First Time)
```bash
cd /Users/iceca/Documents/Weave/backend
python test_complete_flow.py
```

You'll approve each checkpoint manually. Great for learning!

### Auto-Approve Mode (Faster Testing)
```bash
python test_complete_flow.py --auto-approve
```

All checkpoints auto-approved. Great for quick iteration!

---

## Terminal Output Preview

```
=============================================================
WEAVE AGENT SYSTEM - COMPLETE FLOW TEST
=============================================================

STEP 1: Entry Agent (Character Concept)
-------------------------------------------------------------

Entry Agent: Hello! What kind of character would you like to create?

You: A detective who can see ghosts

Entry Agent: Fascinating! Let me help you develop this...
[Interactive Q&A continues]

✓ Entry Agent completed!

STEP 2: Character Development (7 Sub-Agents)
-------------------------------------------------------------

→ Starting character development for 'Morgan Vale'...
✓ Character ID: 550e8400-e29b-41d4-a716-446655440000

Wave 1: Foundation
  [████████████] Personality - DONE
  Checkpoint #1: Psychology profile ready
  Approve? (y/n): y

  [████████████] Backstory - DONE
  Checkpoint #2: Timeline ready
  Approve? (y/n): y

[Continues for all 7 agents...]

✓ Character development complete!
✓ Profile saved to: character_morgan_vale_20251109.json
```

---

## Troubleshooting

### "Cannot connect to API server"
The server isn't running. Open a terminal and run:
```bash
cd /Users/iceca/Documents/Weave/backend
uvicorn api.server:app --port 8000
```

### "Module not found"
Install dependencies:
```bash
cd /Users/iceca/Documents/Weave/backend
pip install -r requirements.txt
```

### "API key not found"
Check your `.env` file has:
```
ANTHROPIC_API_KEY="your-key-here"
GEMINI_API_KEY="your-key-here"
```

---

## Where To Find Results

After testing, you'll find:

1. **Final Profile JSON**
   ```
   /Users/iceca/Documents/Weave/backend/character_yourname_timestamp.json
   ```

2. **All Character Data**
   ```
   /Users/iceca/Documents/Weave/backend/character_data/{character_id}/
   ├── checkpoints/        # All 8 checkpoints
   ├── images/            # Generated character images
   └── final_profile.json # Complete profile
   ```

---

## 🎯 That's It!

Just run these two commands:
```bash
# Terminal 1 (keep open):
cd /Users/iceca/Documents/Weave/backend && uvicorn api.server:app --port 8000

# Terminal 2 (run test):
cd /Users/iceca/Documents/Weave/backend && python test_complete_flow.py
```

Then answer the Entry Agent's questions and watch the magic happen! ✨
