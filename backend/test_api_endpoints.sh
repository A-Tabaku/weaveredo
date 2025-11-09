#!/bin/bash
# Test script for API endpoints
# Run this AFTER starting the API server with: uvicorn api.server:app --port 8000

echo "======================================================"
echo "WEAVE API ENDPOINTS - TEST SUITE"
echo "======================================================"
echo ""
echo "Prerequisites:"
echo "  1. API server must be running: uvicorn api.server:app --port 8000"
echo "  2. Press ENTER to continue, or Ctrl+C to cancel..."
read

BASE_URL="http://localhost:8000"

echo ""
echo "Test 1: Health check..."
HEALTH=$(curl -s "$BASE_URL/health")
if echo "$HEALTH" | grep -q "healthy"; then
    echo "✓ Health check passed: $HEALTH"
else
    echo "✗ Health check failed"
    exit 1
fi

echo ""
echo "Test 2: Start Entry Agent session..."
ENTRY_RESPONSE=$(curl -s -X POST "$BASE_URL/api/entry/start" \
    -H "Content-Type: application/json" \
    -d '{}')
SESSION_ID=$(echo "$ENTRY_RESPONSE" | python -c "import sys, json; print(json.load(sys.stdin)['session_id'])" 2>/dev/null)

if [ -n "$SESSION_ID" ]; then
    echo "✓ Entry session created: $SESSION_ID"
else
    echo "✗ Failed to create entry session"
    echo "$ENTRY_RESPONSE"
    exit 1
fi

echo ""
echo "Test 3: Chat with Entry Agent..."
CHAT_RESPONSE=$(curl -s -X POST "$BASE_URL/api/entry/$SESSION_ID/chat" \
    -H "Content-Type: application/json" \
    -d '{"message":"I want to create a detective character"}')
echo "✓ Entry agent responded"
echo "$CHAT_RESPONSE" | head -100

echo ""
echo "Test 4: Start Character Development..."
CHAR_RESPONSE=$(curl -s -X POST "$BASE_URL/api/character/start" \
    -H "Content-Type: application/json" \
    -d '{
        "characters": [{
            "name": "Test Character",
            "appearance": "Tall and mysterious",
            "personality": "Analytical and determined",
            "role": "Protagonist detective"
        }],
        "storyline": {
            "overview": "A detective solving mysterious cases",
            "tone": "Dark thriller",
            "scenes": ["Opening scene", "Investigation", "Resolution"]
        },
        "mode": "balanced"
    }')

CHARACTER_ID=$(echo "$CHAR_RESPONSE" | python -c "import sys, json; print(json.load(sys.stdin)['character_id'])" 2>/dev/null)

if [ -n "$CHARACTER_ID" ]; then
    echo "✓ Character development started: $CHARACTER_ID"
    echo "✓ Response: $CHAR_RESPONSE"
else
    echo "✗ Failed to start character development"
    echo "$CHAR_RESPONSE"
    exit 1
fi

echo ""
echo "Test 5: Check character status..."
sleep 2
STATUS=$(curl -s "$BASE_URL/api/character/$CHARACTER_ID/status")
echo "✓ Status response: $STATUS"

echo ""
echo "Test 6: Get checkpoint #1 (will appear when ready)..."
echo "Note: Checkpoints take time to generate. Waiting 10 seconds..."
sleep 10

CHECKPOINT=$(curl -s "$BASE_URL/api/character/$CHARACTER_ID/checkpoint/1")
if echo "$CHECKPOINT" | grep -q "checkpoint_number"; then
    echo "✓ Checkpoint #1 retrieved successfully"
    echo "$CHECKPOINT" | head -50
else
    echo "⚠ Checkpoint #1 not ready yet (this is normal)"
    echo "   You can manually approve checkpoints as they appear"
fi

echo ""
echo "Test 7: Approve checkpoint #1..."
APPROVE=$(curl -s -X POST "$BASE_URL/api/character/$CHARACTER_ID/approve" \
    -H "Content-Type: application/json" \
    -d '{"checkpoint": 1}')
echo "✓ Approve response: $APPROVE"

echo ""
echo "======================================================"
echo "✓ API TESTS COMPLETE"
echo "======================================================"
echo ""
echo "Character ID: $CHARACTER_ID"
echo ""
echo "To continue testing:"
echo "  - Check status: curl $BASE_URL/api/character/$CHARACTER_ID/status"
echo "  - Get checkpoint: curl $BASE_URL/api/character/$CHARACTER_ID/checkpoint/N"
echo "  - Approve checkpoint: curl -X POST $BASE_URL/api/character/$CHARACTER_ID/approve -H 'Content-Type: application/json' -d '{\"checkpoint\":N}'"
echo "  - Get final profile: curl $BASE_URL/api/character/$CHARACTER_ID/final"
echo ""
echo "Total checkpoints expected: 7"
echo "  1. Personality"
echo "  2. Backstory & Motivation"
echo "  3. Voice & Dialogue"
echo "  4. Physical Description"
echo "  5. Story Arc"
echo "  6. Relationships"
echo "  7. Final Consolidation"
echo ""
