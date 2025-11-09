# Quick Start Guide - Weave Multi-Agent System

## 🚀 Test Everything NOW

### Option 1: Terminal Flow (Fastest Way to Test)

```bash
cd /Users/iceca/Documents/Weave/backend
python main.py
```

**Flow:**
1. **Entry Agent** asks questions about your video
2. Answer naturally until it outputs JSON
3. Type `/next` → **Character Development** starts automatically
4. **8 Checkpoints** appear - type `y` to approve, `n` to reject, `v` to view full
5. Type `/next` → **Scene Creator** shows mode options
6. Select mode or describe your first scene

---

### Option 2: API Server (For Frontend Integration)

```bash
# Terminal 1: Start API server
cd /Users/iceca/Documents/Weave/backend
uvicorn api.server:app --reload --port 8000

# Terminal 2: Test endpoints
curl http://localhost:8000/health
curl -X POST http://localhost:8000/api/entry/start
```

---

## 📚 Documentation

| File | Purpose |
|------|---------|
| `FRONTEND_INTEGRATION_COMPLETE.md` | Complete React/TypeScript integration guide |
| `IMPLEMENTATION_SUMMARY.md` | What was built and how it works |
| `COMPLETE_TERMINAL_FLOW.md` | Detailed terminal usage guide |
| `UPDATES.md` | Recent changes (Haiku model, checkpoints) |

---

## 🎯 What's Working

- ✅ Entry Agent Q&A (Level 1)
- ✅ Character Development with 8 checkpoints (Level 2)
- ✅ Scene Creator with 3 modes (Level 3)
- ✅ Interactive checkpoint approval (y/n/v)
- ✅ Image generation and display
- ✅ WebSocket real-time updates
- ✅ Complete REST API
- ✅ All agents use Haiku (fast + cheap)

---

## 💡 Key Commands

### In Terminal:
- `/next` - Move to next agent level
- `/reset` - Start over from Entry Agent
- `y` - Approve checkpoint
- `n` - Reject checkpoint (provide feedback)
- `v` - View full checkpoint JSON
- `/mode creative_overview` - Switch Scene Creator mode
- `/mode analytical` - Production quality mode
- `/mode deep_dive` - Maximum control mode

---

## 🔧 API Endpoints

### Entry Agent:
```bash
POST /api/entry/start
POST /api/entry/{session_id}/chat
GET  /api/entry/{session_id}/status
```

### Character Identity:
```bash
POST /api/character/start
GET  /api/character/{id}/status
GET  /api/character/{id}/checkpoint/{num}
POST /api/character/{id}/approve
WS   /ws/character/{id}
```

### Scene Creator:
```bash
POST /api/scene/start
POST /api/scene/{project_id}/chat
POST /api/scene/{project_id}/mode
GET  /api/scene/{project_id}/status
```

---

## 🎨 Frontend Integration

See `FRONTEND_INTEGRATION_COMPLETE.md` for:
- Complete API service layer (TypeScript)
- React components for all agents
- Checkpoint approval UI
- WebSocket integration
- Image display components

Copy-paste ready code included!

---

## 📂 Generated Data

After character development, find generated data at:
```
backend/character_data/{character_id}/
├── input.json                 # Entry Agent output
├── final_profile.json         # Complete character
├── checkpoints/               # All 8 checkpoints
│   ├── 01_personality.json
│   ├── 02_backstory.json
│   └── ...
└── images/                    # Generated images
    ├── portrait.png
    ├── full_body.png
    ├── action.png
    └── expression.png
```

---

## 🔥 Try It Now!

```bash
cd /Users/iceca/Documents/Weave/backend
python main.py
```

Start talking to the Entry Agent and watch the full pipeline in action! 🚀
