"""
Character Development Orchestrator

Manages wave-based execution of 7 sub-agents with checkpoints and human-in-the-loop approval.

Wave Structure:
- Wave 1 (Foundation): Personality + Backstory & Motivation
- Wave 2 (Expression): Voice + Physical + Story Arc
- Wave 3 (Social): Relationships + Image Generation
"""

import asyncio
from datetime import datetime
from typing import Dict, Optional, Callable
import os

from .schemas import (
    CharacterKnowledgeBase,
    Checkpoint,
    CheckpointOutput,
    CheckpointMetadata,
    FinalCharacterProfile,
    CharacterOverview
)
from .storage import CharacterStorage
from .subagents import (
    personality_agent,
    backstory_motivation_agent,
    voice_dialogue_agent,
    physical_description_agent,
    story_arc_agent,
    relationships_agent,
    image_generation_agent
)


class CharacterOrchestrator:
    """Orchestrates wave-based character development"""

    def __init__(
        self,
        character_id: str,
        anthropic_api_key: str,
        gemini_api_key: str,
        storage: CharacterStorage,
        websocket_callback: Optional[Callable] = None
    ):
        self.character_id = character_id
        self.anthropic_api_key = anthropic_api_key
        self.gemini_api_key = gemini_api_key
        self.storage = storage
        self.websocket_callback = websocket_callback  # For real-time updates

        # Load character KB
        self.kb: CharacterKnowledgeBase = storage.load_character_kb(character_id)

    async def _send_update(self, message: Dict):
        """Send real-time update via WebSocket"""
        if self.websocket_callback:
            await self.websocket_callback(message)

    async def _create_checkpoint(
        self,
        checkpoint_number: int,
        agent_name: str,
        wave: int,
        output: Dict,
        narrative: str,
        tokens_used: int,
        agent_time: float
    ) -> Checkpoint:
        """Create and save a checkpoint"""

        checkpoint: Checkpoint = {
            "checkpoint_number": checkpoint_number,
            "agent": agent_name,
            "status": "awaiting_approval",
            "output": {
                "narrative": narrative,
                "structured": output
            },
            "metadata": {
                "wave": wave,
                "timestamp": datetime.utcnow().isoformat(),
                "tokens_used": tokens_used,
                "agent_time_seconds": agent_time
            }
        }

        # Save checkpoint
        self.storage.save_checkpoint(self.character_id, checkpoint)

        # Update metadata
        metadata = self.storage.load_metadata(self.character_id)
        metadata["current_checkpoint"] = checkpoint_number
        self.storage.save_metadata(self.character_id, metadata)

        # Send WebSocket update
        await self._send_update({
            "type": "checkpoint_ready",
            "checkpoint_number": checkpoint_number,
            "agent": agent_name,
            "message": f"{agent_name} analysis complete. Awaiting approval."
        })

        return checkpoint

    async def run_wave_1(self):
        """Execute Wave 1: Foundation (Personality + Backstory)"""

        await self._send_update({
            "type": "wave_started",
            "wave": 1,
            "agents": ["personality", "backstory_motivation"]
        })

        # Update KB
        self.kb["current_wave"] = 1
        self.storage.save_character_kb(self.kb)

        # Run both agents in parallel
        start_time = datetime.now()

        personality_task = personality_agent(self.kb, self.anthropic_api_key)
        backstory_task = backstory_motivation_agent(self.kb, self.anthropic_api_key)

        personality_result, backstory_result = await asyncio.gather(
            personality_task,
            backstory_task
        )

        end_time = datetime.now()
        wave_time = (end_time - start_time).total_seconds()

        # Unpack results
        personality_output, personality_narrative = personality_result
        backstory_output, backstory_narrative = backstory_result

        # Update KB with outputs
        self.kb["personality"] = personality_output
        self.kb["backstory_motivation"] = backstory_output
        self.kb["agent_statuses"]["personality"] = {"status": "completed", "wave": 1}
        self.kb["agent_statuses"]["backstory_motivation"] = {"status": "completed", "wave": 1}
        self.storage.save_character_kb(self.kb)

        # Create checkpoints
        await self._create_checkpoint(
            checkpoint_number=1,
            agent_name="personality",
            wave=1,
            output=personality_output,
            narrative=personality_narrative,
            tokens_used=1500,  # Estimate
            agent_time=wave_time / 2
        )

        await self._create_checkpoint(
            checkpoint_number=2,
            agent_name="backstory_motivation",
            wave=1,
            output=backstory_output,
            narrative=backstory_narrative,
            tokens_used=1800,  # Estimate
            agent_time=wave_time / 2
        )

        await self._send_update({
            "type": "wave_complete",
            "wave": 1,
            "agents_completed": ["personality", "backstory_motivation"],
            "next_wave": 2
        })

    async def run_wave_2(self):
        """Execute Wave 2: Expression (Voice + Physical + Story Arc)"""

        await self._send_update({
            "type": "wave_started",
            "wave": 2,
            "agents": ["voice_dialogue", "physical_description", "story_arc"]
        })

        # Update KB
        self.kb["current_wave"] = 2
        self.storage.save_character_kb(self.kb)

        # Run all three agents in parallel
        start_time = datetime.now()

        voice_task = voice_dialogue_agent(self.kb, self.anthropic_api_key)
        physical_task = physical_description_agent(self.kb, self.anthropic_api_key)
        story_arc_task = story_arc_agent(self.kb, self.anthropic_api_key)

        voice_result, physical_result, story_arc_result = await asyncio.gather(
            voice_task,
            physical_task,
            story_arc_task
        )

        end_time = datetime.now()
        wave_time = (end_time - start_time).total_seconds()

        # Unpack results
        voice_output, voice_narrative = voice_result
        physical_output, physical_narrative = physical_result
        story_arc_output, story_arc_narrative = story_arc_result

        # Update KB
        self.kb["voice_dialogue"] = voice_output
        self.kb["physical_description"] = physical_output
        self.kb["story_arc"] = story_arc_output
        self.kb["agent_statuses"]["voice_dialogue"] = {"status": "completed", "wave": 2}
        self.kb["agent_statuses"]["physical_description"] = {"status": "completed", "wave": 2}
        self.kb["agent_statuses"]["story_arc"] = {"status": "completed", "wave": 2}
        self.storage.save_character_kb(self.kb)

        # Create checkpoints
        await self._create_checkpoint(
            checkpoint_number=3,
            agent_name="voice_dialogue",
            wave=2,
            output=voice_output,
            narrative=voice_narrative,
            tokens_used=1600,
            agent_time=wave_time / 3
        )

        await self._create_checkpoint(
            checkpoint_number=4,
            agent_name="physical_description",
            wave=2,
            output=physical_output,
            narrative=physical_narrative,
            tokens_used=1400,
            agent_time=wave_time / 3
        )

        await self._create_checkpoint(
            checkpoint_number=5,
            agent_name="story_arc",
            wave=2,
            output=story_arc_output,
            narrative=story_arc_narrative,
            tokens_used=1700,
            agent_time=wave_time / 3
        )

        await self._send_update({
            "type": "wave_complete",
            "wave": 2,
            "agents_completed": ["voice_dialogue", "physical_description", "story_arc"],
            "next_wave": 3
        })

    async def run_wave_3(self):
        """Execute Wave 3: Social (Relationships + Image Generation)"""

        await self._send_update({
            "type": "wave_started",
            "wave": 3,
            "agents": ["relationships", "image_generation"]
        })

        # Update KB
        self.kb["current_wave"] = 3
        self.storage.save_character_kb(self.kb)

        # Run both agents in parallel
        start_time = datetime.now()

        relationships_task = relationships_agent(self.kb, self.anthropic_api_key)
        image_task = image_generation_agent(self.kb, self.gemini_api_key, self.storage)

        relationships_result, image_result = await asyncio.gather(
            relationships_task,
            image_task
        )

        end_time = datetime.now()
        wave_time = (end_time - start_time).total_seconds()

        # Unpack results
        relationships_output, relationships_narrative = relationships_result
        image_output, image_narrative = image_result

        # Update KB
        self.kb["relationships"] = relationships_output
        self.kb["image_generation"] = image_output
        self.kb["agent_statuses"]["relationships"] = {"status": "completed", "wave": 3}
        self.kb["agent_statuses"]["image_generation"] = {"status": "completed", "wave": 3}
        self.storage.save_character_kb(self.kb)

        # Create checkpoints
        await self._create_checkpoint(
            checkpoint_number=6,
            agent_name="relationships",
            wave=3,
            output=relationships_output,
            narrative=relationships_narrative,
            tokens_used=1800,
            agent_time=wave_time / 2
        )

        await self._create_checkpoint(
            checkpoint_number=7,
            agent_name="image_generation",
            wave=3,
            output=image_output,
            narrative=image_narrative,
            tokens_used=5160,  # 4 images * 1290 tokens
            agent_time=wave_time / 2
        )

        await self._send_update({
            "type": "wave_complete",
            "wave": 3,
            "agents_completed": ["relationships", "image_generation"],
            "next_wave": "final"
        })

    async def create_final_profile(self) -> FinalCharacterProfile:
        """Consolidate all outputs into final character profile"""

        character = self.kb["input_data"]["characters"][0]
        metadata = self.storage.load_metadata(self.character_id)

        # Create overview
        overview: CharacterOverview = {
            "name": character["name"],
            "role": self.kb["story_arc"]["role"] if self.kb.get("story_arc") else character["role"],
            "importance": 5,  # Can be calculated or configured
            "one_line": f"{character['name']} - {character['role']}"
        }

        # Create visual data
        image_urls = []
        if self.kb.get("image_generation"):
            for img in self.kb["image_generation"]["images"]:
                image_urls.append({
                    "type": img["type"],
                    "url": img["path"]
                })

        visual_data = {
            "images": image_urls,
            "style_notes": self.kb["image_generation"]["style_profile"] if self.kb.get("image_generation") else ""
        }

        # Create final profile
        final_profile: FinalCharacterProfile = {
            "character_id": self.character_id,
            "name": character["name"],
            "version": "1.0",
            "completed_at": datetime.utcnow().isoformat(),
            "overview": overview,
            "visual": visual_data,  # type: ignore
            "psychology": self.kb["personality"],  # type: ignore
            "physical_presence": self.kb["physical_description"],  # type: ignore
            "voice": self.kb["voice_dialogue"],  # type: ignore
            "backstory_motivation": self.kb["backstory_motivation"],  # type: ignore
            "narrative_arc": self.kb["story_arc"],  # type: ignore
            "relationships": self.kb["relationships"]["relationships"] if self.kb.get("relationships") else [],
            "metadata": {
                "mode": self.kb["mode"],
                "development_time_minutes": 0,  # Calculate if needed
                "total_checkpoints": 8,
                "regenerations": metadata.get("regenerations", 0),
                "total_tokens": 12000  # Sum of all agents
            }
        }

        # Save final profile
        self.storage.save_final_profile(self.character_id, final_profile)

        # Create final checkpoint
        await self._create_checkpoint(
            checkpoint_number=8,
            agent_name="final_consolidation",
            wave=4,
            output=final_profile,  # type: ignore
            narrative="Character development complete. All aspects consolidated into comprehensive profile.",
            tokens_used=0,
            agent_time=0.0
        )

        await self._send_update({
            "type": "character_complete",
            "character_id": self.character_id,
            "message": "All agents completed. Character profile ready."
        })

        return final_profile

    async def run_all_waves(self):
        """Execute all waves sequentially"""
        await self.run_wave_1()
        await self.run_wave_2()
        await self.run_wave_3()
        final_profile = await self.create_final_profile()
        return final_profile
