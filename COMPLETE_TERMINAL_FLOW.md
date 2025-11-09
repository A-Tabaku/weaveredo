# Complete Terminal Flow: Entry → Character Development

## How It Works

The system has **2 agent levels** that work together:

1. **Intro_General_Entry** (Level 1) - Gathers video concept + character basics through Q&A
2. **Character_Identity** (Level 2) - Expands characters into full profiles using 7 sub-agents

## Terminal Flow

### Step 1: Start the Terminal

```bash
cd /Users/iceca/Documents/Weave/backend
python main.py
```

### Step 2: Talk to Entry Agent

The Entry Agent will ask you questions about your video concept:

```
[Agent: Intro_General_Entry]

You: I want to create a detective who can see ghosts

Agent: Fascinating! A ghost-seeing detective...
[Interactive Q&A continues]
```

Answer the agent's questions about:
- Characters (name, appearance, personality, role)
- Storyline (concept, key scenes, tone)

### Step 3: Entry Agent Outputs JSON

When you've provided enough info, the agent will automatically output:

```
FINAL OUTPUT:

{
  "characters": [
    {
      "name": "Morgan Vale",
      "appearance": "Tall, gaunt detective in their 30s...",
      "personality": "Haunted, determined...",
      "role": "Protagonist"
    }
  ],
  "storyline": {
    "overview": "A detective who can see ghosts...",
    "tone": "Dark supernatural thriller",
    "scenes": [...]
  }
}

✓ Video concept captured!
✓ 1 character(s) outlined

→ Ready for deep character development!
→ Type '/next' to expand characters with the Character Development system
```

### Step 4: Type `/next` for Character Development

```
You: /next
```

The system will:
1. Switch to Character_Identity agent (Level 2)
2. **Automatically detect** the Entry Agent's JSON
3. **Automatically start** the 7-agent character development pipeline

### Step 5: Watch Character Development

You'll see live progress as 7 AI agents run in 3 waves:

```
[Switched to Agent: Character_Identity]

→ Detected character data from Entry Agent
→ Starting character development automatically...

============================================================
CHARACTER DEVELOPMENT SYSTEM
============================================================

Received character data: Morgan Vale
Starting 7-agent character development pipeline...

Mode: balanced
============================================================

→ Wave 1: Foundation agents starting...
  • Personality agent running...
  ✓ Personality complete

============================================================
Checkpoint #1 Ready
============================================================

Agent: Personality

Narrative:
Morgan Vale exists in the liminal space between life and death...

Structured Data:
  • core_traits: 6 items
  • fears: 4 items
  • secrets: 3 items
  • emotional_baseline: Haunted determination...
  • triggers: 5 items

✓ Checkpoint #1 auto-approved (terminal mode)

[Process continues for all 8 checkpoints...]
```

### Step 6: Character Development Complete

```
============================================================
CHARACTER DEVELOPMENT COMPLETE
============================================================

Character: Morgan Vale
Role: Protagonist

✓ All 8 checkpoints completed
✓ Character profile saved
✓ Images generated

Character data saved to: backend/character_data/{character_id}/

Type '/next' to proceed to Scene Creator, or continue refining this character.
```

## Commands

- `exit` - Quit the program
- `/next` - Move to next agent level
- `/reset` - Reset to Entry Agent

## What Gets Created

After character development, you'll find:

```
backend/character_data/{character_id}/
├── input.json                    # Entry Agent output
├── metadata.json                 # Development tracking
├── knowledge_base.json           # Shared agent knowledge
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
└── final_profile.json            # Complete character
```

## Key Features

✅ **Seamless Integration** - Entry Agent → Character Development with one command
✅ **Automatic Detection** - Character_Identity auto-starts when it sees Entry JSON
✅ **Live Progress** - See each agent and checkpoint as they complete
✅ **Auto-Approval** - Terminal mode auto-approves checkpoints for smooth flow
✅ **Complete Profiles** - 8 checkpoints covering psychology, appearance, voice, backstory, arc, relationships, images
✅ **Persistent Data** - All character data saved to disk

## Example Session

```bash
# Terminal
cd /Users/iceca/Documents/Weave/backend
python main.py

# User talks to Entry Agent about their character
# Entry Agent outputs JSON
# User types: /next
# Character development runs automatically
# Complete character profile generated
```

That's it! 🚀
