#!/bin/bash

# ============================================================================
# Character Development System - Curl Test Script
# ============================================================================
# This script tests the complete character development API workflow
# ============================================================================

set -e  # Exit on error

echo "========================================"
echo "Character Development API Test"
echo "========================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

API_URL="http://localhost:8000/api"

# ============================================================================
# 1. Check if server is running
# ============================================================================
echo -e "${BLUE}[1/8] Checking if API server is running...${NC}"
if curl -s -f "$API_URL/../health" > /dev/null; then
    echo -e "${GREEN}✓ Server is running${NC}"
else
    echo -e "${YELLOW}✗ Server not running. Start with: uvicorn api.server:app --reload --port 8000${NC}"
    exit 1
fi
echo ""

# ============================================================================
# 2. Start character development
# ============================================================================
echo -e "${BLUE}[2/8] Starting character development...${NC}"
START_RESPONSE=$(curl -s -X POST "$API_URL/character/start" \
  -H "Content-Type: application/json" \
  -d @example_data/sample_character_input.json)

CHARACTER_ID=$(echo $START_RESPONSE | jq -r '.character_id')

if [ "$CHARACTER_ID" = "null" ] || [ -z "$CHARACTER_ID" ]; then
    echo -e "${YELLOW}✗ Failed to start character development${NC}"
    echo "Response: $START_RESPONSE"
    exit 1
fi

echo -e "${GREEN}✓ Character development started${NC}"
echo "Character ID: $CHARACTER_ID"
echo ""

# Give agents time to run
echo -e "${YELLOW}⏳ Waiting for agents to process (15 seconds)...${NC}"
sleep 15
echo ""

# ============================================================================
# 3. Check status
# ============================================================================
echo -e "${BLUE}[3/8] Checking character development status...${NC}"
STATUS_RESPONSE=$(curl -s "$API_URL/character/$CHARACTER_ID/status")
echo "$STATUS_RESPONSE" | jq '.'
echo ""

# ============================================================================
# 4. Get Checkpoint #1 (Personality)
# ============================================================================
echo -e "${BLUE}[4/8] Fetching Checkpoint #1 (Personality)...${NC}"
sleep 2
CHECKPOINT_1=$(curl -s "$API_URL/character/$CHARACTER_ID/checkpoint/1")

if echo "$CHECKPOINT_1" | jq -e '.output' > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Checkpoint #1 retrieved${NC}"
    echo "$CHECKPOINT_1" | jq '.output.narrative' -r | head -c 200
    echo "..."
    echo ""
    echo "Structured data:"
    echo "$CHECKPOINT_1" | jq '.output.structured'
else
    echo -e "${YELLOW}⏳ Checkpoint #1 not ready yet${NC}"
fi
echo ""

# ============================================================================
# 5. Approve Checkpoint #1
# ============================================================================
echo -e "${BLUE}[5/8] Approving Checkpoint #1...${NC}"
APPROVE_RESPONSE=$(curl -s -X POST "$API_URL/character/$CHARACTER_ID/approve" \
  -H "Content-Type: application/json" \
  -d '{"checkpoint": 1}')

echo "$APPROVE_RESPONSE" | jq '.'
echo ""

# ============================================================================
# 6. Get Checkpoint #7 (Image Generation)
# ============================================================================
echo -e "${BLUE}[6/8] Fetching Checkpoint #7 (Image Generation)...${NC}"
echo -e "${YELLOW}⏳ Waiting for image generation (30 seconds)...${NC}"
sleep 30

CHECKPOINT_7=$(curl -s "$API_URL/character/$CHARACTER_ID/checkpoint/7")

if echo "$CHECKPOINT_7" | jq -e '.output' > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Checkpoint #7 retrieved${NC}"
    echo "Generated images:"
    echo "$CHECKPOINT_7" | jq '.output.structured.images[] | {type, path}'
else
    echo -e "${YELLOW}⏳ Checkpoint #7 not ready yet (images take longer to generate)${NC}"
fi
echo ""

# ============================================================================
# 7. Check final status
# ============================================================================
echo -e "${BLUE}[7/8] Checking final status...${NC}"
sleep 10

FINAL_STATUS=$(curl -s "$API_URL/character/$CHARACTER_ID/status")
echo "$FINAL_STATUS" | jq '.'
echo ""

# ============================================================================
# 8. Get final character profile
# ============================================================================
echo -e "${BLUE}[8/8] Fetching final character profile...${NC}"
FINAL_PROFILE=$(curl -s "$API_URL/character/$CHARACTER_ID/final")

if echo "$FINAL_PROFILE" | jq -e '.character_id' > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Final profile retrieved${NC}"
    echo ""
    echo "=== CHARACTER PROFILE SUMMARY ==="
    echo "Name: $(echo $FINAL_PROFILE | jq -r '.name')"
    echo "Role: $(echo $FINAL_PROFILE | jq -r '.overview.role')"
    echo "Completed: $(echo $FINAL_PROFILE | jq -r '.completed_at')"
    echo ""
    echo "Psychology:"
    echo $FINAL_PROFILE | jq '.psychology'
    echo ""
    echo "Voice Sample (confident):"
    echo $FINAL_PROFILE | jq -r '.voice.sample_dialogue.confident'
    echo ""
    echo "Images:"
    echo $FINAL_PROFILE | jq '.visual.images'
    echo ""
    echo -e "${GREEN}✓ Test Complete!${NC}"
    echo "Full profile saved at: backend/character_data/$CHARACTER_ID/final_profile.json"
else
    echo -e "${YELLOW}⏳ Final profile not ready yet. Try:${NC}"
    echo "curl http://localhost:8000/api/character/$CHARACTER_ID/final | jq '.'"
fi
echo ""

# ============================================================================
# Test Summary
# ============================================================================
echo "========================================"
echo "Test Summary"
echo "========================================"
echo "Character ID: $CHARACTER_ID"
echo ""
echo "To view data:"
echo "  - Status:     curl http://localhost:8000/api/character/$CHARACTER_ID/status"
echo "  - Checkpoint: curl http://localhost:8000/api/character/$CHARACTER_ID/checkpoint/1"
echo "  - Final:      curl http://localhost:8000/api/character/$CHARACTER_ID/final"
echo ""
echo "To test WebSocket:"
echo "  npm install -g wscat"
echo "  wscat -c ws://localhost:8000/ws/character/$CHARACTER_ID"
echo ""
echo "Data location: ./backend/character_data/$CHARACTER_ID/"
echo ""
