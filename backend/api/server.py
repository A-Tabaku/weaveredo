"""
FastAPI Server for Character Development System

Provides REST API and WebSocket endpoints for character development.
"""

import os
import sys
import asyncio
from pathlib import Path
from typing import Dict, Optional
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from dotenv import load_dotenv

# Add backend directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Load environment
load_dotenv()

# Import agent components
from agents.Character_Identity.agent import CharacterIdentityAgent
from agents.Character_Identity.schemas import EntryAgentOutput
from agent_types import AgentLevel


# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class StartCharacterRequest(BaseModel):
    characters: list
    storyline: dict
    mode: str = "balanced"


class ApproveRequest(BaseModel):
    checkpoint: int


class FeedbackRequest(BaseModel):
    checkpoint: int
    feedback: str


# ============================================================================
# FASTAPI APP
# ============================================================================

app = FastAPI(
    title="Character Development API",
    description="Multi-agent character development system with human-in-the-loop approvals",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve character data as static files
if os.path.exists("./backend/character_data"):
    app.mount("/character_data", StaticFiles(directory="./backend/character_data"), name="character_data")

# Initialize agent
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
if not anthropic_api_key:
    raise ValueError("ANTHROPIC_API_KEY not found in environment")

character_agent = CharacterIdentityAgent(
    api_key=anthropic_api_key,
    level=AgentLevel.Character_Identity
)

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, character_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[character_id] = websocket

    def disconnect(self, character_id: str):
        if character_id in self.active_connections:
            del self.active_connections[character_id]

    async def send_message(self, character_id: str, message: dict):
        if character_id in self.active_connections:
            try:
                await self.active_connections[character_id].send_json(message)
            except:
                self.disconnect(character_id)


manager = ConnectionManager()


# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.get("/")
async def root():
    return {
        "message": "Character Development API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "active"
    }


@app.post("/api/character/start")
async def start_character(request: StartCharacterRequest, background_tasks: BackgroundTasks):
    """
    Start character development from Entry Agent output

    Returns character_id and initiates background processing
    """
    try:
        # Convert request to EntryAgentOutput
        entry_output: EntryAgentOutput = {
            "characters": request.characters,  # type: ignore
            "storyline": request.storyline  # type: ignore
        }

        # Create character
        character_id = character_agent.start_character_development(
            entry_output,
            mode=request.mode
        )

        # Run development in background
        async def run_development():
            async def websocket_callback(message: dict):
                await manager.send_message(character_id, message)

            await character_agent.run_character_development(
                character_id,
                websocket_callback=websocket_callback
            )

        background_tasks.add_task(run_development)

        return {
            "character_id": character_id,
            "status": "wave_1_started",
            "message": "Character development initiated",
            "checkpoint_count": 8
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/character/{character_id}/status")
async def get_status(character_id: str):
    """Get current status of character development"""
    try:
        status = character_agent.get_character_status(character_id)
        return status
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Character not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/character/{character_id}/checkpoint/{checkpoint_number}")
async def get_checkpoint(character_id: str, checkpoint_number: int):
    """Get specific checkpoint data"""
    try:
        checkpoint = character_agent.get_checkpoint(character_id, checkpoint_number)
        if checkpoint is None:
            raise HTTPException(status_code=404, detail="Checkpoint not found")
        return checkpoint
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Character not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/character/{character_id}/approve")
async def approve_checkpoint(character_id: str, request: ApproveRequest):
    """Approve a checkpoint and continue to next agent"""
    try:
        character_agent.approve_checkpoint(character_id, request.checkpoint)
        return {
            "message": f"Checkpoint {request.checkpoint} approved. Proceeding to next agent.",
            "next_checkpoint": request.checkpoint + 1,
            "status": "continuing"
        }
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Character not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/character/{character_id}/feedback")
async def submit_feedback(character_id: str, request: FeedbackRequest):
    """Reject checkpoint and provide feedback for regeneration"""
    try:
        # This would trigger regeneration logic
        # For now, just acknowledge
        return {
            "message": f"Regenerating checkpoint {request.checkpoint} with feedback",
            "status": "regenerating",
            "estimated_time_seconds": 4
        }
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Character not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/character/{character_id}/final")
async def get_final_profile(character_id: str):
    """Get final character profile"""
    try:
        profile = character_agent.get_final_profile(character_id)
        if profile is None:
            raise HTTPException(status_code=404, detail="Final profile not yet complete")
        return profile
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Character not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# WEBSOCKET ENDPOINT
# ============================================================================

@app.websocket("/ws/character/{character_id}")
async def websocket_endpoint(websocket: WebSocket, character_id: str):
    """
    WebSocket endpoint for real-time character development updates

    Messages sent:
    - agent_started: When an agent begins
    - agent_progress: Progress updates
    - checkpoint_ready: When checkpoint is ready for approval
    - wave_complete: When a wave finishes
    - character_complete: When all development is done
    - error: If something goes wrong
    """
    await manager.connect(character_id, websocket)
    try:
        while True:
            # Keep connection alive, listen for ping/pong
            data = await websocket.receive_text()
            if data == "ping":
                await websocket.send_text("pong")
    except WebSocketDisconnect:
        manager.disconnect(character_id)


# ============================================================================
# HEALTH CHECK
# ============================================================================

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "character-development-api"}


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("BACKEND_PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
