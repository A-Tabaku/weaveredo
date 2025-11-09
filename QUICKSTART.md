# Character Development System - Quick Start

## ✅ System Ready!

Your character development multi-agent system is fully implemented and tested.

---

## 🚀 Quick Start (3 Steps)

### 1. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Start FastAPI Server
```bash
uvicorn api.server:app --reload --port 8000
```

### 3. Test with Curl
```bash
# In another terminal
cd backend
./test_curl.sh
```

---

## 📋 What You Have

### ✅ Backend Implementation
- **7 Sub-Agents**: Personality, Backstory, Voice, Physical, Story Arc, Relationships, Image Generation
- **Wave-Based Orchestration**: Foundation → Expression → Social
- **8 Checkpoints**: Human-in-the-loop approval at each stage
- **Gemini Integration**: Generates 4 character images (portrait, full-body, action, expression)
- **FastAPI Server**: REST + WebSocket for real-time updates
- **JSON Storage**: All data persisted in `backend/character_data/`

### ✅ API Endpoints
- `POST /api/character/start` - Start character development
- `GET /api/character/{id}/status` - Check progress
- `GET /api/character/{id}/checkpoint/{num}` - View checkpoint
- `POST /api/character/{id}/approve` - Approve checkpoint
- `POST /api/character/{id}/feedback` - Reject with feedback
- `GET /api/character/{id}/final` - Get final profile
- `WS /ws/character/{id}` - Real-time WebSocket updates

### ✅ Documentation
- [FRONTEND_INTEGRATION.md](FRONTEND_INTEGRATION.md) - Complete API guide for frontend integration
- [backend/agents/Character_Identity/README.md](backend/agents/Character_Identity/README.md) - Architecture details
- [backend/test_curl.sh](backend/test_curl.sh) - Automated test script

---

## 🧪 Testing

### Health Check
```bash
curl http://localhost:8000/health
```

### Start Character Development
```bash
CHARACTER_ID=$(curl -s -X POST http://localhost:8000/api/character/start \
  -H "Content-Type: application/json" \
  -d @backend/example_data/sample_character_input.json \
  | jq -r '.character_id')

echo "Character ID: $CHARACTER_ID"
```

### Check Status
```bash
curl http://localhost:8000/api/character/$CHARACTER_ID/status | jq '.'
```

### Get Checkpoint
```bash
curl http://localhost:8000/api/character/$CHARACTER_ID/checkpoint/1 | jq '.'
```

### View Generated Images
After checkpoint #7 completes:
```bash
# Images stored at:
ls backend/character_data/$CHARACTER_ID/images/
# - portrait.png
# - full_body.png
# - action.png
# - expression.png
```

### Get Final Profile
```bash
curl http://localhost:8000/api/character/$CHARACTER_ID/final | jq '.' > character_profile.json
```

---

## 🌐 Frontend Integration

The system is **ready for frontend integration**. See [FRONTEND_INTEGRATION.md](FRONTEND_INTEGRATION.md) for:
- Complete API documentation
- WebSocket message formats
- ReactFlow tree integration
- Zustand state management
- Component examples

Your existing frontend (React + ReactFlow + Zustand) can integrate seamlessly.

---

## 🔧 Configuration

### Environment Variables (`.env`)
```bash
ANTHROPIC_API_KEY="your-key-here"
GEMINI_API_KEY="your-key-here"
BACKEND_PORT=8000
CHARACTER_DATA_PATH=./backend/character_data
```

✅ Your `.env` is already configured with your API keys!

---

## 📁 Project Structure

```
/backend/
├── api/
│   └── server.py              # FastAPI server
├── agents/
│   └── Character_Identity/
│       ├── agent.py           # Main agent
│       ├── orchestrator.py    # Wave execution
│       ├── storage.py         # JSON persistence
│       ├── schemas.py         # Data structures
│       └── subagents/         # 7 specialized agents
├── character_data/            # Generated character profiles (gitignored)
├── example_data/
│   └── sample_character_input.json
├── test_curl.sh               # Test script
└── requirements.txt

/FRONTEND_INTEGRATION.md      # Complete API guide
/QUICKSTART.md                 # This file
```

---

## 💡 Usage Tips

### Development Modes
```json
{
  "mode": "fast"      // Quick, essential elements only
  "mode": "balanced"  // Default, good depth
  "mode": "deep"      // Maximum detail and questions
}
```

### Wave Execution
- **Wave 1** (Foundation): Runs Personality + Backstory in parallel
- **Wave 2** (Expression): Runs Voice + Physical + Story Arc in parallel
- **Wave 3** (Social): Runs Relationships + Image Generation in parallel

Each wave waits for previous wave to complete before starting.

---

## 🐛 Troubleshooting

### Server won't start
```bash
# Check if port 8000 is in use
lsof -i :8000

# Try different port
uvicorn api.server:app --reload --port 8001
```

### Import errors
```bash
# Run from backend directory
cd backend
python -c "from api.server import app; print('✓ Imports OK')"
```

### API key issues
```bash
# Verify .env file exists and has keys
cat .env | grep API_KEY
```

---

## 📊 Expected Output

### Checkpoint Example (Personality)
```json
{
  "checkpoint_number": 1,
  "agent": "personality",
  "output": {
    "narrative": "Cole is fundamentally guilt-ridden...",
    "structured": {
      "core_traits": ["guilt-ridden", "resourceful", "cynical"],
      "fears": ["betrayal", "becoming his past self"],
      "secrets": ["still steals when stressed"],
      ...
    }
  }
}
```

### Final Profile
Comprehensive JSON with:
- Psychology (personality, fears, triggers)
- Physical presence (mannerisms, body language)
- Voice (speech patterns, sample dialogue)
- Backstory & motivation (timeline, goals)
- Story arc (role, transformation beats)
- Relationships (character connections)
- Visual (4 generated images)

---

## 🚀 Next Steps

1. **Test the system**: Run `./test_curl.sh`
2. **Explore the API**: Check `/docs` for interactive Swagger UI
3. **Integrate frontend**: Use [FRONTEND_INTEGRATION.md](FRONTEND_INTEGRATION.md)
4. **Customize**: Modify sub-agent prompts for your specific needs

---

## 📚 Documentation Links

- [Frontend Integration Guide](FRONTEND_INTEGRATION.md) - Complete API docs
- [Character_Identity README](backend/agents/Character_Identity/README.md) - Architecture
- [FastAPI Docs](http://localhost:8000/docs) - Interactive API explorer (when server running)

---

**System Status: ✅ READY FOR PRODUCTION USE**

All components implemented, tested, and documented. The character development system is fully operational!
