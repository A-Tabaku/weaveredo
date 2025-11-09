# Character Development System - Frontend Integration Guide

## 🎯 Overview

This guide explains how to integrate the Character Development multi-agent system into your existing React + ReactFlow + Zustand frontend.

The character system takes input from the Entry Agent and expands a character through 7 specialized sub-agents, each providing checkpoints for human-in-the-loop approval.

---

## 🏗️ Architecture

```
Entry Agent (Level 1) → Outputs Character JSON
    ↓
Character_Identity Agent (Level 2) → Orchestrates 7 Sub-Agents
    ├─ Wave 1: Personality + Backstory (Foundation)
    ├─ Wave 2: Voice + Physical + Story Arc (Expression)
    └─ Wave 3: Relationships + Image Gen (Social)
    ↓
8 Checkpoints for User Approval
    ↓
Complete Character Profile with Images
```

---

## 📡 API Endpoints

### Base URL
```
http://localhost:8000/api
```

### 1. Start Character Development
```http
POST /character/start
Content-Type: application/json

Request Body:
{
  "characters": [{
    "name": "Cole",
    "appearance": "Rugged male cowboy in his 30s-40s...",
    "personality": "Silent and mysterious...",
    "role": "The cowboy who claims the hat..."
  }],
  "storyline": {
    "overview": "A cinematic Western cowboy hat advertisement...",
    "tone": "Cinematic and dramatic",
    "scenes": [...]
  },
  "mode": "balanced"  // Optional: "fast" | "balanced" | "deep"
}

Response (201 Created):
{
  "character_id": "uuid-here",
  "status": "wave_1_started",
  "message": "Character development initiated",
  "checkpoint_count": 8
}
```

### 2. Get Current Status
```http
GET /character/{character_id}/status

Response (200 OK):
{
  "character_id": "uuid-here",
  "current_wave": 1,
  "current_agent": "personality",
  "status": "in_progress",  // "in_progress" | "awaiting_approval" | "completed"
  "progress": {
    "completed_checkpoints": 0,
    "total_checkpoints": 8,
    "current_checkpoint": 1
  },
  "agents": {
    "personality": {"status": "in_progress", "wave": 1},
    "backstory_motivation": {"status": "pending", "wave": 1},
    "voice_dialogue": {"status": "pending", "wave": 2},
    "physical_description": {"status": "pending", "wave": 2},
    "story_arc": {"status": "pending", "wave": 2},
    "relationships": {"status": "pending", "wave": 3},
    "image_generation": {"status": "pending", "wave": 3}
  }
}
```

### 3. Get Checkpoint Data
```http
GET /character/{character_id}/checkpoint/{number}

Response (200 OK):
{
  "checkpoint_number": 1,
  "agent": "personality",
  "status": "awaiting_approval",
  "output": {
    "narrative": "Cole is fundamentally guilt-ridden, carrying the weight of his criminal past like chains. He's resourceful—street-smart survival instincts honed from years on the edge. A cynical exterior masks deep fear of betrayal and terror of regressing to who he once was.",
    "structured": {
      "core_traits": ["guilt-ridden", "resourceful", "cynical", "loyal"],
      "fears": ["betrayal by those he trusts", "becoming his past self again"],
      "secrets": ["still steals when stressed (muscle memory)", "knows the crime boss who ruined his family"],
      "emotional_baseline": "guarded but yearning for connection",
      "triggers": ["mentions of family", "symbols of authority", "old haunts"]
    }
  },
  "metadata": {
    "wave": 1,
    "timestamp": "2025-11-08T14:32:10Z",
    "tokens_used": 1250,
    "agent_time_seconds": 3.2
  }
}
```

### 4. Approve Checkpoint
```http
POST /character/{character_id}/approve
Content-Type: application/json

Request Body:
{
  "checkpoint": 1
}

Response (200 OK):
{
  "message": "Checkpoint 1 approved. Proceeding to next agent.",
  "next_checkpoint": 2,
  "status": "continuing"
}
```

### 5. Reject with Feedback (Regenerate)
```http
POST /character/{character_id}/feedback
Content-Type: application/json

Request Body:
{
  "checkpoint": 1,
  "feedback": "Make Cole more sarcastic and add a sense of dark humor to his personality"
}

Response (200 OK):
{
  "message": "Regenerating personality agent with feedback",
  "status": "regenerating",
  "estimated_time_seconds": 4
}
```

### 6. Get Final Character Profile
```http
GET /character/{character_id}/final

Response (200 OK):
{
  "character_id": "uuid-here",
  "name": "Cole",
  "version": "1.0",
  "completed_at": "2025-11-08T14:45:00Z",

  "overview": {
    "name": "Cole",
    "role": "Protagonist - Reformed thief seeking redemption",
    "importance": 5,
    "one_line": "A guilt-ridden former thief who claims a mysterious cowboy hat and rides toward redemption"
  },

  "visual": {
    "images": [
      {"type": "portrait", "url": "/character_data/uuid/images/portrait.png"},
      {"type": "full_body", "url": "/character_data/uuid/images/full_body.png"},
      {"type": "action", "url": "/character_data/uuid/images/action.png"},
      {"type": "expression", "url": "/character_data/uuid/images/expression.png"}
    ],
    "style_notes": "Realistic cinematic Western photography, rugged and weathered aesthetic"
  },

  "psychology": {
    "core_traits": ["guilt-ridden", "resourceful", "cynical", "loyal"],
    "fears": ["betrayal", "becoming his past self"],
    "secrets": ["still steals when stressed"],
    "emotional_baseline": "guarded but yearning",
    "triggers": ["family mentions", "authority symbols"]
  },

  "physical_presence": {
    "mannerisms": ["always scanning exits", "fidgets with rings when nervous", "tilts hat when suspicious"],
    "body_language": "Cautious posture, shoulders slightly hunched, hands near pockets",
    "movement_style": "Deliberate and quiet, minimizing sound",
    "physical_quirks": ["cracks knuckles before tense moments", "rubs scar on chin when thinking"]
  },

  "voice": {
    "speech_pattern": "Informal with street slang, deflects with humor, fragments sentences under stress",
    "verbal_tics": ["Look...", "Whatever", "*nervous laugh*", "Ain't"],
    "vocabulary": "Working-class vernacular mixed with old Western expressions",
    "sample_dialogue": {
      "confident": "Look, I know what you're thinking. But whatever, I've got this handled.",
      "vulnerable": "I just... I can't let people down again. Not this time.",
      "stressed": "*nervous laugh* Yeah, totally fine. Why wouldn't I be fine?",
      "sarcastic": "Oh sure, because trusting people has worked out great for me before."
    }
  },

  "backstory_motivation": {
    "timeline": [
      {"age": 12, "event": "Father arrested, family fell apart"},
      {"age": 16, "event": "First theft - stole to feed siblings"},
      {"age": 22, "event": "Became professional thief, worked for crime boss"},
      {"age": 28, "event": "The job that broke him - innocent person hurt"},
      {"age": 30, "event": "Walked away from criminal life"},
      {"age": 32, "event": "Present day - seeking redemption"}
    ],
    "formative_experiences": [
      "Watching his father taken away shaped his distrust of authority",
      "Survival as a street kid taught him resourcefulness",
      "The incident where someone got hurt shattered his moral compartmentalization"
    ],
    "goals": {
      "surface": "Survive, stay free, don't look back",
      "deep": "Prove to himself he can be better than his past, find belonging"
    },
    "internal_conflicts": ["Wanting connection vs fear of betrayal", "Self-loathing vs desire for redemption"]
  },

  "narrative_arc": {
    "role": "Protagonist",
    "arc_type": "Redemption arc",
    "transformation_beats": [
      {"act": 1, "beat": "Claims the hat - symbolic acceptance of new identity"},
      {"act": 2, "beat": "Tested by old associates - temptation to return"},
      {"act": 2, "beat": "Makes sacrifice for community - chooses others over self"},
      {"act": 3, "beat": "Confronts past - faces the people he hurt"},
      {"act": 3, "beat": "Achieves redemption - forgives himself"}
    ],
    "scene_presence": ["Opening (hat claiming)", "Midpoint confrontation", "Climax sacrifice", "Resolution"]
  },

  "relationships": [
    {
      "character": "The Mentor (TBD - unnamed)",
      "type": "mentor_figure",
      "dynamic": "The person who believes in Cole when he doesn't believe in himself",
      "evolution": "Initial skepticism → trust → deep bond"
    },
    {
      "character": "The Crime Boss (TBD)",
      "type": "antagonist",
      "dynamic": "Represents Cole's past and what he could become",
      "evolution": "Former employer → threat → final confrontation"
    },
    {
      "character": "Family (estranged)",
      "type": "family_conflict",
      "dynamic": "Broken relationships from his criminal years",
      "evolution": "No contact → attempted reconciliation → forgiveness"
    }
  ],

  "metadata": {
    "mode": "balanced",
    "development_time_minutes": 8,
    "total_checkpoints": 8,
    "regenerations": 1,
    "total_tokens": 12450
  }
}
```

---

## 🔌 WebSocket Real-Time Updates

### Connection
```javascript
const ws = new WebSocket(`ws://localhost:8000/ws/character/${characterId}`);
```

### Message Types

#### 1. Agent Started
```json
{
  "type": "agent_started",
  "agent": "personality",
  "wave": 1,
  "timestamp": "2025-11-08T14:30:00Z"
}
```

#### 2. Agent Progress
```json
{
  "type": "agent_progress",
  "agent": "personality",
  "status": "generating_traits",
  "progress": 30,
  "message": "Analyzing core personality traits..."
}
```

#### 3. Checkpoint Ready
```json
{
  "type": "checkpoint_ready",
  "checkpoint_number": 1,
  "agent": "personality",
  "message": "Personality analysis complete. Awaiting approval."
}
```

#### 4. Wave Complete
```json
{
  "type": "wave_complete",
  "wave": 1,
  "agents_completed": ["personality", "backstory_motivation"],
  "next_wave": 2
}
```

#### 5. Character Complete
```json
{
  "type": "character_complete",
  "character_id": "uuid-here",
  "message": "All agents completed. Character profile ready."
}
```

#### 6. Error
```json
{
  "type": "error",
  "error": "Gemini API rate limit exceeded",
  "agent": "image_generation",
  "recoverable": true
}
```

---

## 🌳 ReactFlow Tree Integration

### Tree Structure

```
Character: Cole (Root Node)
├─ Wave 1: Foundation
│   ├─ Personality (checkpoint #1)
│   └─ Backstory & Motivation (checkpoint #2)
├─ Wave 2: Expression
│   ├─ Voice & Dialogue (checkpoint #3)
│   ├─ Physical Description (checkpoint #4)
│   └─ Story Arc (checkpoint #5)
└─ Wave 3: Social
    ├─ Relationships (checkpoint #6)
    └─ Image Generation (checkpoint #7)
```

### Node Data Structure

```typescript
interface CharacterTreeNode {
  id: string;
  name: string;
  type: 'character_root' | 'wave' | 'agent';
  status: 'pending' | 'in_progress' | 'awaiting_approval' | 'completed';
  progress?: number;  // 0-100
  checkpoint?: number;
  wave?: number;
  metadata?: {
    agent?: string;
    lastUpdate?: string;
    tokensUsed?: number;
  };
}
```

### Example ReactFlow Nodes

```typescript
const characterNodes: Node[] = [
  {
    id: 'root',
    type: 'character_root',
    data: {
      name: 'Cole',
      status: 'in_progress',
      progress: 25
    },
    position: { x: 0, y: 0 }
  },
  {
    id: 'wave_1',
    type: 'wave',
    data: {
      name: 'Wave 1: Foundation',
      status: 'in_progress',
      wave: 1
    },
    position: { x: -200, y: 100 },
    parentNode: 'root'
  },
  {
    id: 'agent_personality',
    type: 'agent',
    data: {
      name: 'Personality',
      status: 'completed',
      checkpoint: 1,
      wave: 1,
      metadata: {
        agent: 'personality',
        tokensUsed: 1250
      }
    },
    position: { x: -300, y: 200 },
    parentNode: 'wave_1'
  },
  {
    id: 'agent_backstory',
    type: 'agent',
    data: {
      name: 'Backstory & Motivation',
      status: 'awaiting_approval',
      checkpoint: 2,
      wave: 1,
      progress: 100
    },
    position: { x: -100, y: 200 },
    parentNode: 'wave_1'
  }
];
```

---

## 💾 State Management with Zustand

### Character Store

```typescript
// src/store/characterStore.ts
import { create } from 'zustand';

interface CharacterDevelopment {
  id: string;
  name: string;
  status: 'in_progress' | 'completed';
  currentWave: number;
  currentCheckpoint: number;
  checkpoints: Map<number, CheckpointData>;
  finalProfile?: FinalCharacterProfile;
}

interface CharacterStore {
  characters: Map<string, CharacterDevelopment>;
  activeCharacterId: string | null;

  // Actions
  startCharacterDevelopment: (input: EntryAgentOutput) => Promise<string>;
  setActiveCharacter: (id: string) => void;
  updateCharacterStatus: (id: string, status: any) => void;
  addCheckpoint: (characterId: string, checkpoint: CheckpointData) => void;
  approveCheckpoint: (characterId: string, checkpointNum: number) => Promise<void>;
  rejectCheckpoint: (characterId: string, checkpointNum: number, feedback: string) => Promise<void>;
  getFinalProfile: (characterId: string) => Promise<FinalCharacterProfile>;
}

export const useCharacterStore = create<CharacterStore>((set, get) => ({
  characters: new Map(),
  activeCharacterId: null,

  startCharacterDevelopment: async (input) => {
    const response = await fetch('http://localhost:8000/api/character/start', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(input)
    });
    const data = await response.json();

    set(state => {
      const newChar: CharacterDevelopment = {
        id: data.character_id,
        name: input.characters[0].name,
        status: 'in_progress',
        currentWave: 1,
        currentCheckpoint: 0,
        checkpoints: new Map()
      };
      state.characters.set(data.character_id, newChar);
      return { characters: state.characters, activeCharacterId: data.character_id };
    });

    return data.character_id;
  },

  approveCheckpoint: async (characterId, checkpointNum) => {
    await fetch(`http://localhost:8000/api/character/${characterId}/approve`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ checkpoint: checkpointNum })
    });
  },

  rejectCheckpoint: async (characterId, checkpointNum, feedback) => {
    await fetch(`http://localhost:8000/api/character/${characterId}/feedback`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ checkpoint: checkpointNum, feedback })
    });
  },

  // ... other actions
}));
```

---

## 🎨 Component Examples

### 1. Character Development View

```typescript
// src/components/character/CharacterDevelopmentView.tsx
import { useEffect, useState } from 'react';
import { useCharacterStore } from '@/store/characterStore';
import { CharacterTree } from './CharacterTree';
import { CheckpointPanel } from './CheckpointPanel';

export function CharacterDevelopmentView() {
  const { activeCharacterId, characters } = useCharacterStore();
  const [ws, setWs] = useState<WebSocket | null>(null);

  useEffect(() => {
    if (!activeCharacterId) return;

    // Connect WebSocket for real-time updates
    const websocket = new WebSocket(`ws://localhost:8000/ws/character/${activeCharacterId}`);

    websocket.onmessage = (event) => {
      const message = JSON.parse(event.data);
      handleWebSocketMessage(message);
    };

    setWs(websocket);
    return () => websocket.close();
  }, [activeCharacterId]);

  return (
    <div className="character-development-view">
      <CharacterTree characterId={activeCharacterId} />
      <CheckpointPanel characterId={activeCharacterId} />
    </div>
  );
}
```

### 2. Checkpoint Approval Component

```typescript
// src/components/character/CheckpointPanel.tsx
import { useCharacterStore } from '@/store/characterStore';
import { useState } from 'react';

export function CheckpointPanel({ characterId }: { characterId: string }) {
  const { characters, approveCheckpoint, rejectCheckpoint } = useCharacterStore();
  const [feedback, setFeedback] = useState('');

  const character = characters.get(characterId);
  if (!character) return null;

  const currentCheckpoint = character.checkpoints.get(character.currentCheckpoint);
  if (!currentCheckpoint || currentCheckpoint.status !== 'awaiting_approval') {
    return <div>No checkpoint awaiting approval</div>;
  }

  return (
    <div className="checkpoint-panel">
      <h2>Checkpoint #{currentCheckpoint.checkpoint_number}: {currentCheckpoint.agent}</h2>

      <div className="checkpoint-output">
        <h3>Narrative</h3>
        <p>{currentCheckpoint.output.narrative}</p>

        <h3>Structured Data</h3>
        <pre>{JSON.stringify(currentCheckpoint.output.structured, null, 2)}</pre>
      </div>

      <div className="checkpoint-actions">
        <button
          onClick={() => approveCheckpoint(characterId, currentCheckpoint.checkpoint_number)}
          className="approve-button"
        >
          ✓ Approve
        </button>

        <div className="feedback-section">
          <textarea
            placeholder="Provide feedback for regeneration..."
            value={feedback}
            onChange={(e) => setFeedback(e.target.value)}
          />
          <button
            onClick={() => {
              rejectCheckpoint(characterId, currentCheckpoint.checkpoint_number, feedback);
              setFeedback('');
            }}
            disabled={!feedback}
            className="reject-button"
          >
            ↻ Regenerate with Feedback
          </button>
        </div>
      </div>
    </div>
  );
}
```

### 3. Image Gallery Component (Checkpoint #7)

```typescript
// src/components/character/ImageGallery.tsx
import { useState } from 'react';

export function ImageGallery({ checkpoint }: { checkpoint: ImageCheckpoint }) {
  const [selectedImages, setSelectedImages] = useState<Set<string>>(new Set());

  const toggleImage = (type: string) => {
    const newSet = new Set(selectedImages);
    if (newSet.has(type)) {
      newSet.delete(type);
    } else {
      newSet.add(type);
    }
    setSelectedImages(newSet);
  };

  return (
    <div className="image-gallery">
      <h2>Generated Character Images</h2>
      <p>Select at least 2 images to approve</p>

      <div className="image-grid">
        {checkpoint.output.images.map((img) => (
          <div
            key={img.type}
            className={`image-card ${selectedImages.has(img.type) ? 'selected' : ''}`}
            onClick={() => toggleImage(img.type)}
          >
            <img src={`http://localhost:8000${img.url}`} alt={img.type} />
            <div className="image-info">
              <h3>{img.type}</h3>
              <p className="prompt-preview">{img.prompt.slice(0, 100)}...</p>
              {selectedImages.has(img.type) && <span className="checkmark">✓</span>}
            </div>
          </div>
        ))}
      </div>

      <button
        disabled={selectedImages.size < 2}
        onClick={() => approveImages(Array.from(selectedImages))}
      >
        Approve Selected ({selectedImages.size}/4)
      </button>
    </div>
  );
}
```

---

## 🎨 Styling Notes

### Status Colors (existing design system)
- **Pending**: Purple (`#9333EA`)
- **In Progress**: Blue (`#3B82F6`)
- **Awaiting Approval**: Orange (`#F59E0B`)
- **Completed**: Green (`#10B981`)

### Node Styling
Use existing ReactFlow custom node styles with checkpoint-specific badges:

```css
.character-node {
  background: linear-gradient(135deg, #2D2D32 0%, #252528 100%);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  padding: 16px;
}

.checkpoint-badge {
  position: absolute;
  top: -8px;
  right: -8px;
  background: var(--status-color);
  border-radius: 50%;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: bold;
}
```

---

## 🧪 Testing the Integration

### 1. Start Development Server
```bash
cd backend
uvicorn api.server:app --reload --port 8000
```

### 2. Test with curl (before frontend integration)
```bash
# Start character development
CHARACTER_ID=$(curl -s -X POST http://localhost:8000/api/character/start \
  -H "Content-Type: application/json" \
  -d @example_data/sample_character_input.json \
  | jq -r '.character_id')

# Monitor status
curl http://localhost:8000/api/character/$CHARACTER_ID/status

# Get checkpoint
curl http://localhost:8000/api/character/$CHARACTER_ID/checkpoint/1

# Approve
curl -X POST http://localhost:8000/api/character/$CHARACTER_ID/approve \
  -H "Content-Type: application/json" \
  -d '{"checkpoint": 1}'
```

### 3. Frontend Integration Test
```typescript
// In your app
const characterId = await useCharacterStore.getState().startCharacterDevelopment({
  characters: [{ name: "Test", appearance: "...", personality: "...", role: "..." }],
  storyline: { overview: "...", tone: "...", scenes: [] }
});

// Watch WebSocket messages in DevTools
```

---

## 🚀 Quick Start Checklist

- [ ] Backend server running on port 8000
- [ ] `.env` file configured with API keys
- [ ] Add `characterStore.ts` to Zustand state management
- [ ] Create `CharacterDevelopmentView` component
- [ ] Integrate with existing ReactFlow tree
- [ ] Add WebSocket connection logic
- [ ] Style checkpoint panels with existing design system
- [ ] Test full flow: start → checkpoints → approval → final profile

---

## 📚 Additional Resources

- **Backend API Code**: `/backend/api/server.py`
- **Agent Implementation**: `/backend/agents/Character_Identity/`
- **Example Data**: `/backend/example_data/sample_character_input.json`
- **Curl Test Script**: `/backend/test_curl.sh`

---

**Questions or issues? Check the README in `/backend/agents/Character_Identity/` for detailed architecture documentation.**
