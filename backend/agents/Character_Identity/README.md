# Character_Identity Agent

Multi-agent character development system that expands basic character concepts into comprehensive, psychologically-rich profiles.

## Overview

The Character_Identity agent takes input from the Entry Agent (Level 1) and develops it through 7 specialized sub-agents organized in 3 waves:

- **Wave 1 (Foundation)**: Personality + Backstory & Motivation
- **Wave 2 (Expression)**: Voice & Dialogue + Physical Description + Story Arc
- **Wave 3 (Social)**: Relationships + Image Generation

Each agent produces a checkpoint for human-in-the-loop approval.

## Architecture

```
EntryAgent Output (JSON)
    ↓
CharacterIdentityAgent.start_character_development()
    ↓
Orchestrator manages 3 waves:
    Wave 1 → Checkpoints #1, #2
    Wave 2 → Checkpoints #3, #4, #5
    Wave 3 → Checkpoints #6, #7
    Final → Checkpoint #8
    ↓
FinalCharacterProfile (comprehensive JSON + images)
```

## Components

### Core Files
- `agent.py` - Main Character_Identity agent class
- `orchestrator.py` - Wave-based execution controller
- `storage.py` - JSON file persistence layer
- `schemas.py` - TypedDict data structures

### Sub-Agents (`subagents/`)
1. **personality.py** - Core traits, fears, secrets, emotional baseline
2. **backstory_motivation.py** - Timeline, formative events, goals
3. **voice_dialogue.py** - Speech patterns, sample dialogue
4. **physical_description.py** - Mannerisms, body language, movement
5. **story_arc.py** - Narrative role, transformation beats
6. **relationships.py** - Character connections and dynamics
7. **image_generation.py** - Gemini API integration for visual generation

## API Usage

### Start Character Development
```python
from agents.Character_Identity.agent import CharacterIdentityAgent
from agent_types import AgentLevel

agent = CharacterIdentityAgent(
    api_key=anthropic_api_key,
    level=AgentLevel.Character_Identity
)

character_id = agent.start_character_development(
    entry_output={
        "characters": [...],
        "storyline": {...}
    },
    mode="balanced"
)

# Run async
import asyncio
final_profile = asyncio.run(
    agent.run_character_development(character_id)
)
```

### REST API (FastAPI)
See [FRONTEND_INTEGRATION.md](/FRONTEND_INTEGRATION.md) for complete API documentation.

```bash
# Start server
cd backend
uvicorn api.server:app --reload --port 8000

# Start character development
curl -X POST http://localhost:8000/api/character/start \
  -H "Content-Type: application/json" \
  -d @example_data/sample_character_input.json

# Check status
curl http://localhost:8000/api/character/{character_id}/status

# Get checkpoint
curl http://localhost:8000/api/character/{character_id}/checkpoint/1

# Get final profile
curl http://localhost:8000/api/character/{character_id}/final
```

## Data Flow

1. **Input**: Entry Agent JSON with character + storyline
2. **Processing**: 7 sub-agents run in waves with checkpoints
3. **Output**: Comprehensive character profile with:
   - Psychological depth (personality, backstory, motivation)
   - Physical presence (appearance, mannerisms, movement)
   - Narrative function (story arc, role, transformation)
   - Social dynamics (relationships)
   - Visual representation (4 generated images)

## Storage

Character data stored in `/backend/character_data/{character_id}/`:
```
character_data/
└── {character_id}/
    ├── input.json              # Original Entry Agent output
    ├── metadata.json           # Status, timestamps, progress
    ├── knowledge_base.json     # Shared data across sub-agents
    ├── checkpoints/
    │   ├── 01_personality.json
    │   ├── 02_backstory.json
    │   ├── ...
    │   └── 08_final.json
    ├── images/
    │   ├── portrait.png
    │   ├── full_body.png
    │   ├── action.png
    │   └── expression.png
    └── final_profile.json      # Complete character profile
```

## Development Modes

- **Fast**: Essential elements only, fewer questions, faster execution
- **Balanced** (default): Good depth with efficiency
- **Deep**: Maximum detail and complexity, thorough analysis

## Testing

```bash
# Run complete test suite with curl
cd backend
./test_curl.sh

# Or manually test individual endpoints
curl http://localhost:8000/health
```

## Environment Variables

Required in `.env`:
```bash
ANTHROPIC_API_KEY="sk-ant-..."
GEMINI_API_KEY="AIza..."
BACKEND_PORT=8000
CHARACTER_DATA_PATH=./backend/character_data
```

## Dependencies

- `anthropic>=0.39.0` - Claude API
- `google-generativeai>=0.3.0` - Gemini image generation
- `fastapi>=0.104.0` - REST API
- `uvicorn>=0.24.0` - ASGI server
- `websockets>=12.0` - Real-time updates
- `python-dotenv>=1.0.0` - Environment management

## Future Enhancements

- Regeneration with feedback (currently stubbed)
- Character version history and branching
- Multi-character relationship matrix
- Export to different formats (PDF, Markdown)
- Custom sub-agent configuration

## Related Documentation

- [Frontend Integration Guide](/FRONTEND_INTEGRATION.md)
- [API Server](../api/server.py)
- [Example Data](../example_data/sample_character_input.json)
- [Test Script](../test_curl.sh)
