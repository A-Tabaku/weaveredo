#!/bin/bash
# Test script for terminal interface
# Tests that main.py can start and basic functionality works

echo "======================================================"
echo "WEAVE TERMINAL INTERFACE - QUICK TEST"
echo "======================================================"
echo ""

echo "Test 1: Check Python imports..."
python -c "
from main import main, get_agent_by_level
from agent_types import AgentLevel
from agents.Character_Identity.agent import CharacterIdentityAgent
from agents.Character_Identity.subagents import (
    personality_agent,
    backstory_motivation_agent,
    voice_dialogue_agent,
    physical_description_agent,
    story_arc_agent,
    relationships_agent
)
print('✓ All imports successful')
" || { echo "✗ Import test failed"; exit 1; }

echo ""
echo "Test 2: Check API keys in .env..."
if [ ! -f .env ]; then
    echo "✗ .env file not found"
    exit 1
fi

if grep -q "ANTHROPIC_API_KEY=" .env; then
    echo "✓ ANTHROPIC_API_KEY found"
else
    echo "✗ ANTHROPIC_API_KEY missing"
    exit 1
fi

if grep -q "GEMINI_API_KEY=" .env; then
    echo "✓ GEMINI_API_KEY found"
else
    echo "✗ GEMINI_API_KEY missing"
    exit 1
fi

echo ""
echo "Test 3: Check directory structure..."
[ -d "backend/character_data" ] || mkdir -p "backend/character_data"
echo "✓ character_data directory exists"

[ -d "agents/Character_Identity/subagents" ] || { echo "✗ subagents directory missing"; exit 1; }
echo "✓ subagents directory exists"

echo ""
echo "======================================================"
echo "✓ All pre-flight checks passed!"
echo "======================================================"
echo ""
echo "To run terminal interface:"
echo "  python main.py"
echo ""
echo "Expected flow:"
echo "  1. Entry Agent asks questions"
echo "  2. Answer naturally until JSON output"
echo "  3. Type '/next' to start Character Development"
echo "  4. See 6 checkpoints (personality, backstory, voice, physical, story_arc, relationships)"
echo "  5. Type 'y' to approve each checkpoint"
echo "  6. Final checkpoint (#7) consolidates everything"
echo ""
echo "Commands:"
echo "  y - Approve checkpoint"
echo "  n - Reject checkpoint (with feedback)"
echo "  v - View full checkpoint JSON"
echo "  e - Edit checkpoint inline"
echo "  /next - Move to next agent level"
echo "  /reset - Start over"
echo "  exit - Quit"
echo ""
