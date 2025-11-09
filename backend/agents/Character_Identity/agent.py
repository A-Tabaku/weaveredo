"""
Character_Identity Agent (Level 2)

Main agent class for character development system.
Takes input from Entry Agent (Level 1) and expands character through 7 specialized sub-agents.

This agent:
1. Receives character overview from Entry Agent
2. Initializes character development session
3. Orchestrates 7 sub-agents in wave-based execution
4. Manages checkpoints and human-in-the-loop approval
5. Returns comprehensive character profile

Note: This agent DOES NOT replace or modify the Entry Agent (Level 1).
It operates as a separate, subsequent stage in the pipeline.
"""

import os
import asyncio
from typing import Optional, List, Dict
from dotenv import load_dotenv

from agent_types import AgentLevel
from .schemas import EntryAgentOutput, FinalCharacterProfile
from .storage import CharacterStorage
from .orchestrator import CharacterOrchestrator


class CharacterIdentityAgent:
    """
    Character Development Agent (Level 2)

    Expands basic character concepts into fully-developed character profiles
    with psychological depth, visual representation, and narrative function.
    """

    def __init__(self, api_key: str, level: AgentLevel):
        """
        Initialize Character Identity Agent

        Args:
            api_key: Anthropic API key
            level: AgentLevel enum (should be AgentLevel.Character_Identity)
        """
        self.anthropic_api_key = api_key
        self.level = level

        # Load additional API keys from environment
        load_dotenv()
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")

        if not self.gemini_api_key:
            raise ValueError("GEMINI_API_KEY not found in environment")

        # Initialize storage
        self.storage = CharacterStorage()

        # Track active character sessions
        self.active_sessions: Dict[str, CharacterOrchestrator] = {}

    def start_character_development(
        self,
        entry_output: EntryAgentOutput,
        mode: str = "balanced"
    ) -> str:
        """
        Start character development from Entry Agent output

        Args:
            entry_output: Output from Entry Agent (Level 1)
            mode: Development mode (fast/balanced/deep)

        Returns:
            character_id: UUID of created character session
        """
        # Create character in storage
        character_id = self.storage.create_character(entry_output, mode)
        return character_id

    async def run_character_development(
        self,
        character_id: str,
        websocket_callback: Optional = None
    ) -> FinalCharacterProfile:
        """
        Execute full character development for a character

        Args:
            character_id: Character UUID
            websocket_callback: Optional callback for real-time updates

        Returns:
            FinalCharacterProfile: Complete character profile
        """
        # Create orchestrator
        orchestrator = CharacterOrchestrator(
            character_id=character_id,
            anthropic_api_key=self.anthropic_api_key,
            gemini_api_key=self.gemini_api_key,
            storage=self.storage,
            websocket_callback=websocket_callback
        )

        # Store active session
        self.active_sessions[character_id] = orchestrator

        try:
            # Run all waves
            final_profile = await orchestrator.run_all_waves()
            return final_profile
        finally:
            # Clean up session
            if character_id in self.active_sessions:
                del self.active_sessions[character_id]

    def get_character_status(self, character_id: str) -> Dict:
        """
        Get current status of character development

        Args:
            character_id: Character UUID

        Returns:
            Dict with status information
        """
        metadata = self.storage.load_metadata(character_id)
        kb = self.storage.load_character_kb(character_id)

        return {
            "character_id": character_id,
            "current_wave": kb["current_wave"],
            "current_checkpoint": metadata["current_checkpoint"],
            "status": metadata["status"],
            "progress": {
                "completed_checkpoints": metadata["completed_checkpoints"],
                "total_checkpoints": metadata["total_checkpoints"],
                "current_checkpoint": metadata["current_checkpoint"]
            },
            "agents": kb["agent_statuses"]
        }

    def get_checkpoint(self, character_id: str, checkpoint_number: int):
        """
        Get specific checkpoint data

        Args:
            character_id: Character UUID
            checkpoint_number: Checkpoint number (1-8)

        Returns:
            Checkpoint data or None
        """
        return self.storage.load_checkpoint(character_id, checkpoint_number)

    def approve_checkpoint(self, character_id: str, checkpoint_number: int):
        """
        Approve a checkpoint and allow continuation

        Args:
            character_id: Character UUID
            checkpoint_number: Checkpoint number to approve
        """
        metadata = self.storage.load_metadata(character_id)
        metadata["completed_checkpoints"] = checkpoint_number
        self.storage.save_metadata(character_id, metadata)

    async def regenerate_agent(
        self,
        character_id: str,
        agent_name: str,
        feedback: str
    ):
        """
        Regenerate a specific agent with user feedback

        Args:
            character_id: Character UUID
            agent_name: Name of agent to regenerate
            feedback: User feedback for regeneration
        """
        # Update regeneration count
        metadata = self.storage.load_metadata(character_id)
        metadata["regenerations"] = metadata.get("regenerations", 0) + 1
        self.storage.save_metadata(character_id, metadata)

        # TODO: Implement regeneration logic
        # This would re-run specific agent with feedback incorporated
        # into the prompt
        pass

    def get_final_profile(self, character_id: str) -> Optional[FinalCharacterProfile]:
        """
        Get final character profile

        Args:
            character_id: Character UUID

        Returns:
            FinalCharacterProfile or None if not yet complete
        """
        return self.storage.load_final_profile(character_id)

    async def run(self, user_input: str, conversation_history: List[Dict]) -> str:
        """
        Main run method for terminal-based interface (legacy compatibility)

        Note: This agent is primarily designed for API usage, not terminal chat.
        Use the API endpoints for full functionality.

        Args:
            user_input: User input string
            conversation_history: Conversation history

        Returns:
            Response string
        """
        return """Character Identity Agent (Level 2)

This agent develops detailed character profiles from Entry Agent output.

For full functionality, use the API endpoints:
- POST /api/character/start - Start character development
- GET  /api/character/{id}/status - Check progress
- GET  /api/character/{id}/checkpoint/{num} - View checkpoint
- POST /api/character/{id}/approve - Approve checkpoint
- GET  /api/character/{id}/final - Get final profile

Run the FastAPI server:
  cd backend
  uvicorn api.server:app --reload --port 8000

See FRONTEND_INTEGRATION.md for complete API documentation.
"""
