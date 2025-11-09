# Terminal Testing Guide - Complete Flow

## 🎯 Overview

This guide shows you how to test the **complete Weave agent pipeline** from Entry Agent to Character Development, all in your terminal.

---

## 🚀 Quick Start

### Prerequisites
1. **Server must be running:**
   ```bash
   cd backend
   uvicorn api.server:app --port 8000
   ```

2. **API keys configured** in `.env`:
   ```bash
   ANTHROPIC_API_KEY="your-key"
   GEMINI_API_KEY="your-key"
   ```

### Run Complete Flow Test
```bash
cd backend
python test_complete_flow.py
```

**With auto-approval** (faster testing):
```bash
python test_complete_flow.py --auto-approve
```

---

## 📋 What The Test Does

The script runs the **complete pipeline**:

```
┌─────────────────────────────────────┐
│ STEP 1: Entry Agent                 │
│ - Interactive Q&A with user         │
│ - Builds character concept          │
│ - Outputs JSON                      │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ STEP 2: Character Development       │
│ - Calls API with Entry JSON         │
│ - Starts 7 sub-agents               │
│ - Returns character_id              │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ STEP 3: Live Progress Monitoring    │
│ Wave 1: Foundation                   │
│   → Personality [✓] Checkpoint #1   │
│   → Backstory [✓] Checkpoint #2     │
│                                     │
│ Wave 2: Expression                   │
│   → Voice [✓] Checkpoint #3         │
│   → Physical [✓] Checkpoint #4      │
│   → Story Arc [✓] Checkpoint #5     │
│                                     │
│ Wave 3: Social                       │
│   → Relationships [✓] Checkpoint #6 │
│   → Images [✓] Checkpoint #7        │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ STEP 4: Final Character Profile     │
│ - Complete JSON output              │
│ - Generated images                  │
│ - Saved to file                     │
└─────────────────────────────────────┘
```

---

## 💬 Example Session

### Step 1: Entry Agent Interaction
```
=============================================================
STEP 1: Entry Agent (Character Concept)
-------------------------------------------------------------

Entry Agent: Hello! I'm here to help you develop a character.
What kind of character would you like to create?

You: I want to create a detective who can see ghosts

Entry Agent: Fascinating! A ghost-seeing detective could be really
compelling. Let me help you develop this concept...

What's the overall concept or theme?
1. A supernatural detective solving ghost-related mysteries?
2. A regular detective haunted by ghosts of victims?
3. A character torn between two worlds?

You: Number 1, a supernatural detective

Entry Agent: Great! Now let's build out the character...

[Interactive Q&A continues until JSON is generated]

✓ Entry Agent completed! Character JSON generated.
```

### Step 2: Character Development Starts
```
=============================================================
STEP 2: Character Development (7 Sub-Agents)
-------------------------------------------------------------

→ Starting character development for 'Detective Morgan Vale'...
✓ Character ID: 550e8400-e29b-41d4-a716-446655440000
→ Status: wave_1_started
→ Total checkpoints: 8
```

### Step 3: Live Progress
```
→ Monitoring character development progress...
→ Agents are running in parallel waves...

Wave 1: Foundation (Personality + Backstory)

=============================================================
Checkpoint #1: Personality
=============================================================

Narrative:
Morgan Vale exists in the liminal space between life and death,
their consciousness forever altered by a near-death experience...

Structured Data:
  • core_traits: 6 items
  • fears: 4 items
  • secrets: 3 items
  • emotional_baseline: Haunted determination mixed with...
  • triggers: 5 items

Approve checkpoint #1? (y/n): y

✓ Checkpoint #1 approved. Continuing...

[Process continues for all 8 checkpoints]
```

### Step 4: Final Output
```
=============================================================
STEP 3: Final Character Profile
-------------------------------------------------------------

✓ Character development complete!

Character: Morgan Vale
Role: Protagonist - Supernatural detective
Completed: 2025-11-09T01:30:45Z

✓ Profile saved to: character_morgan_vale_20251109_013045.json

Character Highlights:

  Traits: haunted determination, empathetic observer, boundary-walker
  Fears: losing humanity, being pulled into death permanently

  Sample Dialogue: "The dead don't lie, detective.
  That's more than I can say for the living."

  Generated Images: 4
    • portrait: /character_data/{id}/images/portrait.png
    • full_body: /character_data/{id}/images/full_body.png
    • action: /character_data/{id}/images/action.png
    • expression: /character_data/{id}/images/expression.png

→ Full character data: backend/character_data/{id}/

=============================================================
TEST COMPLETE!
=============================================================
✓ Full pipeline tested successfully!
```

---

## 🎮 Interactive Controls

### During Entry Agent
- **Answer questions naturally** - The agent will guide you
- **Be detailed** - More detail = better character development
- **Wait for JSON** - Agent will output structured data when ready

### During Character Development
- **Auto-approve mode** (`--auto-approve`):
  - All checkpoints approved automatically
  - Faster testing
  - Use for quick iteration

- **Manual approval mode** (default):
  - Review each checkpoint
  - Approve with `y`
  - Reject with `n` and provide feedback
  - Regeneration happens automatically

### Interrupting
- **Ctrl+C** - Stop monitoring (data is saved)
- Can resume by checking character_id status via API

---

## 📁 Output Files

### Generated Files
```
backend/
├── character_morgan_vale_20251109_013045.json  # Final profile
└── character_data/
    └── {character_id}/
        ├── input.json                           # Entry Agent input
        ├── metadata.json                        # Status tracking
        ├── knowledge_base.json                  # Shared agent data
        ├── checkpoints/
        │   ├── 01_personality.json
        │   ├── 02_backstory_motivation.json
        │   ├── 03_voice_dialogue.json
        │   ├── 04_physical_description.json
        │   ├── 05_story_arc.json
        │   ├── 06_relationships.json
        │   ├── 07_image_generation.json
        │   └── 08_final_consolidation.json
        ├── images/
        │   ├── portrait.png
        │   ├── full_body.png
        │   ├── action.png
        │   └── expression.png
        └── final_profile.json
```

---

## 🔧 Troubleshooting

### Server Not Running
```
✗ Cannot connect to API server. Is it running?
→ Start server with: uvicorn api.server:app --port 8000
```

**Solution:**
```bash
cd backend
uvicorn api.server:app --port 8000
```

### API Key Missing
```
✗ ANTHROPIC_API_KEY not found in environment
```

**Solution:**
Check `.env` file has:
```bash
ANTHROPIC_API_KEY="your-key"
GEMINI_API_KEY="your-key"
```

### Checkpoint Not Ready
```
⚠ Final profile not yet ready. Waiting...
```

**This is normal** - agents are still processing. The script will retry automatically.

### Entry Agent Doesn't Finalize
If Entry Agent keeps asking questions and never outputs JSON:
- Make sure you're providing complete answers
- The agent needs enough information to create the JSON
- Try being more specific in your responses

---

## 💡 Tips for Best Results

### Entry Agent Tips
1. **Be specific** about character appearance and personality
2. **Include story context** - tone, setting, role
3. **Describe key scenes** if you have them in mind
4. **Answer follow-up questions** - they improve quality

### Character Development Tips
1. **Use balanced mode** (default) for good quality without too many questions
2. **Use deep mode** for maximum detail (slower)
3. **Use fast mode** for quick prototyping
4. **Review checkpoints carefully** - early corrections prevent later issues
5. **Provide specific feedback** when rejecting - helps regeneration

---

## 🔄 Testing Different Scenarios

### Test 1: Quick Character (Auto-Approve)
```bash
python test_complete_flow.py --auto-approve
```
Best for: Rapid iteration, testing system functionality

### Test 2: Detailed Character (Manual Approval)
```bash
python test_complete_flow.py
```
Best for: Quality control, understanding agent outputs

### Test 3: Different Modes
Modify the API call in the script to test different modes:
```python
# In start_character_development():
response = requests.post(
    "http://localhost:8000/api/character/start",
    json={**entry_json, "mode": "deep"}  # or "fast"
)
```

---

## 📊 Understanding The Output

### Checkpoint Structure
Each checkpoint contains:
- **Narrative**: Human-readable description (2-3 paragraphs)
- **Structured**: Machine-readable data (JSON)
- **Metadata**: Wave number, tokens used, timing

### Final Profile
Complete character with:
- Overview (name, role, importance)
- Visual (4 generated images + style notes)
- Psychology (traits, fears, secrets, triggers)
- Physical presence (mannerisms, body language)
- Voice (speech patterns, sample dialogue)
- Backstory & motivation (timeline, goals)
- Narrative arc (role, transformation)
- Relationships (character connections)

---

## 🚀 Next Steps

After successful terminal testing:
1. **Review generated characters** in `character_data/`
2. **Integrate with frontend** using [FRONTEND_INTEGRATION.md](../FRONTEND_INTEGRATION.md)
3. **Customize sub-agents** if needed
4. **Add to your pipeline** - Entry → Character → Scene Creator (future)

---

## 📚 Related Documentation

- [QUICKSTART.md](../QUICKSTART.md) - Quick setup guide
- [FRONTEND_INTEGRATION.md](../FRONTEND_INTEGRATION.md) - Frontend integration
- [SYSTEM_TESTED_AND_WORKING.md](../SYSTEM_TESTED_AND_WORKING.md) - Verification
- [agents/Character_Identity/README.md](agents/Character_Identity/README.md) - Architecture

---

**Happy testing! 🎉**
