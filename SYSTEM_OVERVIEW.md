# Weave Multi-Agent Video Generation System - Complete Overview

## What Is This System?

Weave is a **multi-agent AI orchestration system** for video generation that maintains consistency across scenes and characters. It uses a **3-level agent hierarchy** to transform a user's video concept into production-ready specifications.

### The Problem It Solves

Video generation tools like Sora are inconsistent for long-form content:
- Characters look different between scenes
- Visual continuity breaks
- No narrative coherence
- Manual specification is tedious

### The Solution

Weave uses **specialized AI agents** that work together to:
1. Gather video concept through natural conversation
2. Develop detailed, consistent character profiles
3. Create scene-by-scene specifications with cinematography
4. Maintain continuity across the entire video

---

## Three-Level Agent Hierarchy

### Level 1: Entry Agent (`Intro_General_Entry`)
**Purpose:** Conversational information gathering
**Model:** claude-haiku-4-5-20251001
**What it does:**
- Asks natural questions about the video concept
- Gathers character details (name, appearance, personality, role)
- Gathers storyline details (overview, scenes, tone)
- Autonomously decides when it has enough information
- Outputs structured JSON for next agent

**Example Interaction:**
```
User: I want to create a detective character
Agent: Great! Let's develop this. What's the detective's name?
User: Morgan Vale
Agent: Tell me about Morgan's appearance...
[...continues Q&A...]
Agent: [Outputs complete JSON]
```

**Output Format:**
```json
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
    "scenes": ["Scene 1...", "Scene 2..."]
  }
}
```

---

### Level 2: Character Identity Agent
**Purpose:** Deep character development through specialized sub-agents
**Model:** claude-haiku-4-5-20251001 (all sub-agents)
**What it does:**
- Takes Entry Agent JSON as input
- Runs **7 specialized sub-agents** in **3 parallel waves**
- Creates **8 checkpoints** with human-in-the-loop approval
- Generates **4 character images** (portrait, full-body, action, expression)
- Outputs comprehensive character profile

#### The 7 Sub-Agents

**Wave 1: Foundation** (runs in parallel)
1. **Personality** - Core traits, fears, secrets, emotional baseline, triggers
2. **Backstory & Motivation** - Timeline, formative experiences, goals (surface + deep), internal conflicts

**Wave 2: Expression** (runs in parallel)
3. **Voice & Dialogue** - Speech patterns, vocabulary, sample dialogue, communication style
4. **Physical Description** - Detailed appearance, mannerisms, body language, movement style
5. **Story Arc** - Narrative function, transformation beats, character journey

**Wave 3: Social** (runs in parallel)
6. **Relationships** - Connections to other characters, dynamics, relationship arcs
7. **Image Generation** - Uses Gemini API to generate 4 visual references

#### Wave Execution Flow

```
Entry JSON received
  ↓
Wave 1 starts: Personality + Backstory run simultaneously
  ↓
Personality completes → Checkpoint #1 created
  ↓
System WAITS for user approval (y/n/v/e)
  ↓
User approves → Checkpoint #1 approved
  ↓
Backstory completes → Checkpoint #2 created
  ↓
System WAITS for user approval
  ↓
User approves → Wave 1 complete
  ↓
Wave 2 starts: Voice + Physical + Story Arc run simultaneously
  ↓
[Checkpoints #3, #4, #5 - each waits for approval]
  ↓
Wave 3 starts: Relationships + Image Gen run simultaneously
  ↓
[Checkpoints #6, #7 - each waits for approval]
  ↓
Final consolidation → Checkpoint #8
  ↓
Complete character profile saved
```

#### Checkpoint Interaction

At each checkpoint, user can:
- **`y`** - Approve and continue
- **`n`** - Reject with feedback (then continues)
- **`v`** - View full narrative + complete JSON
- **`e`** - Edit structured data inline

**Example Checkpoint:**
```
============================================================
Checkpoint #1 Ready
============================================================

Agent: Personality

Narrative:
Morgan Vale exists in a state of perpetual analysis, their mind
constantly processing evidence both visible and spectral...
[800 character preview]

Structured Data:
  • core_traits: 6 items
    - Hypervigilant analyst
    - Compartmentalized identity
    ... and 4 more
  • fears: 4 items
  • secrets: 3 items
  • emotional_baseline: Haunted determination
  • triggers: 5 items

────────────────────────────────────────────────────────────
Approve? (y/n/v/e):
```

#### Inline Editing (`e` option)

```
→ Edit mode for Personality
Enter new value (or press Enter to keep current):

core_traits (currently 6 items):
  1. Hypervigilant analyst
  2. Compartmentalized identity
  3. Defensive humor user

Edit core_traits? (y/n): y
Enter new items (one per line, empty line when done):
  - Strategic thinker
  - Emotionally guarded
  - Detail-oriented
  -

✓ Updated core_traits
✓ Checkpoint saved with edits!
```

#### Final Output Structure

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
└── final_profile.json            # Complete character profile
```

---

### Level 3: Scene Creator Agent
**Purpose:** Generate detailed scene specifications with cinematography
**Model:** claude-haiku-4-5-20251001
**What it does:**
- Takes character profiles from Level 2 (optional)
- Creates scene-by-scene specifications
- Generates cinematography (shots, angles, movements)
- Defines lighting, color, audio
- Validates continuity
- Generates reference images via Gemini

#### Three Personality Modes

User selects mode at start:

1. **Creative Overview** (Fast)
   - 2-3 concept generation → rapid execution
   - Minimal checkpoints (5-7 messages total)
   - Best for: Prototyping, exploration, speed

2. **Analytical** (Quality)
   - Comprehensive pre/post validation (30+ checks)
   - Blocks generation on critical issues
   - Best for: Production quality, client work

3. **Deep Dive** (Control)
   - 2 options for every major decision
   - Modular approval (narrative, location, cinematography, lighting, color, audio)
   - 15-25 messages with granular control
   - Best for: Learning, perfectionism, precise control

#### Character Data Access

Scene Creator can call `get_character_data` tool to access:
```json
{
  "character_id": "abc-123",
  "name": "Morgan Vale",
  "physical_details": {
    "height": "5'10\"",
    "build": "lean",
    "distinctive_features": [...]
  },
  "personality": {
    "core_traits": [...],
    "emotional_baseline": "..."
  },
  "image_prompts": [...]
}
```

This ensures visual and behavioral consistency in scenes.

#### Scene Output

```json
{
  "scene_number": 1,
  "duration": "45s",
  "narrative": "Morgan enters the abandoned warehouse...",
  "cinematography": {
    "shots": [
      {
        "type": "wide",
        "duration": "3s",
        "camera_movement": "slow dolly in",
        "angle": "low angle",
        "description": "Establishing shot of warehouse exterior"
      },
      ...
    ]
  },
  "lighting": {
    "setup": "High contrast noir lighting",
    "key_light": "Hard moonlight through windows",
    "color_temperature": "Cool blue (5600K)"
  },
  "color_palette": ["#1a1a2e", "#16213e", "#0f3460", "#e94560"],
  "audio": {
    "ambient": "Wind, distant traffic",
    "sfx": ["Footsteps on concrete", "Door creak"],
    "music": "Tense atmospheric score"
  },
  "veo_parameters": { ... }
}
```

---

## Complete Terminal Flow

### Step 1: Start Terminal
```bash
cd /Users/iceca/Documents/Weave/backend
python main.py
```

### Step 2: Entry Agent Conversation
```
Weave Agent System
Type 'exit' to quit, '/next' to move to next agent, '/reset' to restart
------------------------------------------------------------
[Agent: Intro_General_Entry]

You: I want to create a detective who can see ghosts

Agent: Fascinating! A ghost-seeing detective. Let me help you develop this.
       What's the detective's name?

You: Morgan Vale

Agent: Great! Tell me about Morgan's physical appearance...

[...Q&A continues...]

Agent: FINAL OUTPUT:

{
  "characters": [
    {
      "name": "Morgan Vale",
      "appearance": "Tall, gaunt detective in their 30s with perpetually tired eyes...",
      "personality": "Haunted, determined, uses dark humor as defense mechanism",
      "role": "Protagonist detective who bridges living and dead"
    }
  ],
  "storyline": {
    "overview": "A detective who can see ghosts uses their ability to solve cold cases...",
    "tone": "Dark supernatural thriller",
    "scenes": [
      "Morgan discovers a new ghost at a crime scene",
      "The ghost leads Morgan to hidden evidence",
      "Confrontation with the killer"
    ]
  }
}

✓ Video concept captured!
✓ 1 character(s) outlined

→ Ready for deep character development!
→ Type '/next' to expand characters with the Character Development system
```

### Step 3: Character Development
```
You: /next

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
Morgan Vale exists in a state of perpetual analysis...

Structured Data:
  • core_traits: 6 items
    - Hypervigilant analyst
    - Compartmentalized identity
    - Defensive humor as shield
    - Boundary walker (living/dead)
    - Evidence-driven rationalist
    - Emotionally self-protective
  • fears: 4 items
    - Loss of sanity
    - Being unable to help ghosts
    - Becoming trapped between worlds
    - Losing connection to the living
  • secrets: 3 items
  • emotional_baseline: Haunted determination mixed with exhaustion
  • triggers: 5 items

────────────────────────────────────────────────────────────
Approve? (y/n/v/e): y

✓ Checkpoint #1 approved

  • Backstory agent running...
  ✓ Backstory complete

============================================================
Checkpoint #2 Ready
============================================================

[...continues through all 8 checkpoints...]

============================================================
CHARACTER DEVELOPMENT COMPLETE
============================================================

Character: Morgan Vale
Role: Protagonist detective who bridges living and dead

✓ All 8 checkpoints completed
✓ Character profile saved
✓ Images generated

Character data saved to: backend/character_data/abc-123-def-456/

Type '/next' to proceed to Scene Creator, or continue refining this character.
```

### Step 4: Scene Creation
```
You: /next

[Switched to Agent: Scene_Creator]

→ Detected completed character profiles
→ Ready for scene creation!

Scene Creator Modes:
  /mode creative_overview - Fast prototyping (2-3 concepts → rapid execution)
  /mode analytical        - Production quality (comprehensive validation)
  /mode deep_dive         - Maximum control (2 options per decision)

Or just describe your first scene to start with default mode.

You: /mode creative_overview

Agent: Mode switched to creative_overview. Let's create scenes quickly!
       What's the first scene you envision?

You: Morgan enters an abandoned warehouse and sees a ghost

Agent: [Uses get_character_data tool to fetch Morgan's appearance]
       [Uses cinematography_designer to generate shot sequences]
       [Uses aesthetic_generator for lighting/color]

       Great! I see Morgan Vale is tall, gaunt, with tired eyes.
       For this warehouse scene, I'm thinking:

       Option 1: High contrast noir with...
       Option 2: Desaturated documentary style with...

       Which approach feels right?

[...scene creation continues...]
```

---

## Backend Architecture

### API Endpoints

**Entry Agent:**
```
POST   /api/entry/start
POST   /api/entry/{session_id}/chat
GET    /api/entry/{session_id}/status
```

**Character Identity:**
```
POST   /api/character/start
GET    /api/character/{id}/status
GET    /api/character/{id}/checkpoint/{num}
POST   /api/character/{id}/approve
POST   /api/character/{id}/feedback
GET    /api/character/{id}/final
WS     /ws/character/{id}          # Real-time updates
```

**Scene Creator:**
```
POST   /api/scene/start
POST   /api/scene/{project_id}/chat
POST   /api/scene/{project_id}/mode
GET    /api/scene/{project_id}/status
```

**Projects:**
```
POST   /api/projects
GET    /api/projects
GET    /api/projects/{id}
```

### WebSocket Updates (Character Development)

Real-time messages sent during character development:
```json
{"type": "wave_started", "wave": 1, "agents": ["personality", "backstory"]}
{"type": "agent_started", "agent": "personality"}
{"type": "agent_completed", "agent": "personality"}
{"type": "checkpoint_ready", "checkpoint_number": 1, "agent": "personality"}
{"type": "wave_complete", "wave": 1}
{"type": "character_complete"}
```

---

## Key Features

### 1. **Human-in-the-Loop Checkpoints**
- Every agent output requires approval
- User can view full details, edit, or reject
- System waits for approval before continuing
- No automatic progression

### 2. **Inline Editing**
- Edit structured data directly in terminal
- Add/remove/replace list items
- Modify string values
- Changes saved to checkpoint files

### 3. **Knowledge Base Propagation**
- Each agent sees all previous agent outputs
- Later agents build on earlier work
- Ensures consistency across the profile

### 4. **Wave-Based Execution**
- Agents run in parallel within waves
- Prevents conflicts (e.g., Voice doesn't run before Personality)
- Maximizes speed while maintaining logic

### 5. **Character Data Access for Scene Creator**
- Scene Creator can query character profiles
- Uses `get_character_data` tool
- Ensures visual/behavioral continuity in scenes

### 6. **Multi-Modal Output**
- Text narratives (human-readable)
- Structured JSON (machine-readable)
- Generated images (visual references)
- All saved and accessible

---

## File Structure

```
/Users/iceca/Documents/Weave/
├── backend/
│   ├── main.py                            # Terminal interface
│   ├── agent_types.py                     # AgentLevel enum
│   ├── .env                               # API keys
│   ├── api/
│   │   └── server.py                      # FastAPI REST + WebSocket
│   ├── agents/
│   │   ├── Intro_General_Entry/
│   │   │   └── agent.py                   # Entry Agent
│   │   ├── Character_Identity/
│   │   │   ├── agent.py                   # Main orchestrator
│   │   │   ├── orchestrator.py            # Wave execution
│   │   │   ├── storage.py                 # File persistence
│   │   │   ├── schemas.py                 # TypedDict schemas
│   │   │   └── subagents/
│   │   │       ├── personality.py
│   │   │       ├── backstory_motivation.py
│   │   │       ├── voice_dialogue.py
│   │   │       ├── physical_description.py
│   │   │       ├── story_arc.py
│   │   │       ├── relationships.py
│   │   │       └── image_generation.py
│   │   └── Scene_Creator/
│   │       ├── agent.py                   # Main scene agent
│   │       ├── tools.py                   # Tool definitions
│   │       ├── modes/
│   │       │   ├── creative_overview.py
│   │       │   ├── analytical.py
│   │       │   └── deep_dive.py
│   │       └── subagents/
│   │           └── subagent.py            # 7 specialized tools
│   ├── utils/
│   │   └── state_manager.py              # Project state management
│   ├── character_data/                    # Generated characters
│   │   └── {character_id}/
│   │       ├── input.json
│   │       ├── checkpoints/
│   │       ├── images/
│   │       └── final_profile.json
│   └── state/
│       ├── projects/                      # Project state files
│       └── scenes/                        # Scene specifications
├── frontend/                              # React app (ready for integration)
│   ├── src/
│   │   ├── components/
│   │   │   ├── tree/                      # ReactFlow visualization
│   │   │   ├── chat/                      # Chat components
│   │   │   └── layout/                    # Layout components
│   │   ├── store/
│   │   │   └── useStore.ts                # Zustand state
│   │   └── types/
│   │       └── index.ts                   # TypeScript types
│   └── package.json
└── DOCS/
    ├── FRONTEND_INTEGRATION_COMPLETE.md   # Complete frontend guide
    ├── COMPLETE_SYSTEM_READY.md           # Bug fixes & features
    ├── SYSTEM_OVERVIEW.md                 # This file
    ├── IMPLEMENTATION_SUMMARY.md          # Quick reference
    └── QUICK_START.md                     # How to run
```

---

## Models Used

All agents use **claude-haiku-4-5-20251001**:
- **10-20x faster** than Sonnet
- **~80% cost reduction**
- Still high-quality for structured tasks

Image generation uses **Gemini 2.5 Flash** (via Nano Banana API):
- Character portraits
- Full-body references
- Action poses
- Expression sheets

---

## Frontend Integration

Complete TypeScript/React guide available in [FRONTEND_INTEGRATION_COMPLETE.md](FRONTEND_INTEGRATION_COMPLETE.md).

Includes:
- API service layer
- Zustand store integration
- React components for all 3 agents
- Checkpoint approval UI
- WebSocket real-time updates
- Image display
- Mode selection

**All code is copy-paste ready.**

---

## How To Use

### Terminal Mode (Quickest)
```bash
cd /Users/iceca/Documents/Weave/backend
python main.py

# Talk to Entry Agent
# Type /next for Character Development
# Approve checkpoints with y/n/v/e
# Type /next for Scene Creator
```

### API Mode (For Frontend)
```bash
# Terminal 1: Start API server
cd /Users/iceca/Documents/Weave/backend
uvicorn api.server:app --reload --port 8000

# Terminal 2: Use frontend
cd /Users/iceca/Documents/Weave/frontend
npm run dev
```

### Commands
- `/next` - Move to next agent level
- `/reset` - Start over from Entry Agent
- `/mode creative_overview` - Switch Scene Creator mode
- `y` - Approve checkpoint
- `n` - Reject checkpoint
- `v` - View full checkpoint JSON
- `e` - Edit checkpoint inline
- `exit` - Quit

---

## What Makes This Unique

1. **Multi-Agent Orchestration** - Specialized agents collaborate
2. **Human-in-the-Loop** - Every output requires approval
3. **Inline Editing** - Modify AI outputs directly
4. **Wave-Based Execution** - Parallel processing with logical ordering
5. **Knowledge Base Sharing** - Agents build on each other's work
6. **Character Continuity** - Scene Creator accesses character data
7. **Multi-Modal Output** - Text, JSON, and images
8. **Three Modes** - Choose speed vs. control
9. **Complete API** - REST + WebSocket for real-time updates
10. **Production Ready** - Tested, documented, deployable

---

## Status

✅ **All systems operational**
✅ **Terminal flow tested and working**
✅ **API endpoints complete**
✅ **Frontend guide ready**
✅ **Documentation complete**

**Next step:** Implement frontend using [FRONTEND_INTEGRATION_COMPLETE.md](FRONTEND_INTEGRATION_COMPLETE.md)

---

## Summary

Weave transforms a simple idea into production-ready video specifications through:

**Entry Agent** → Gathers concept via conversation
↓
**Character Development** → 7 agents create comprehensive profiles
↓
**Scene Creator** → Generates cinematography with character continuity
↓
**Video Specifications** → Ready for generation

**All with human oversight at every step.**

This is a complete, production-ready AI orchestration system for video generation. 🚀
