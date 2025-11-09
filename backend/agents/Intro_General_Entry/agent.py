"""
Entry agent for Weave - gathers initial video concept information.
Single LLM system that asks questions and outputs structured JSON when ready.
"""

from typing import List, Dict, Any
import json
from anthropic import AsyncAnthropic  # FIX: Use AsyncAnthropic for async functions
from agent_types import AgentLevel


class EntryAgent:
    """Entry agent that gathers video concept details through conversation"""

    def __init__(self, api_key: str, level: AgentLevel):
        self.api_key = api_key
        self.level = level
        self.client = AsyncAnthropic(api_key=api_key)  # FIX: Use AsyncAnthropic for async functions
        self.model = "claude-haiku-4-5-20251001"  # Using Haiku for speed + cost efficiency

    async def run(self, user_input: str, conversation_history: List[Dict[str, str]]) -> str:
        """
        Main execution method - conversational Q&A until ready to output JSON

        Args:
            user_input: User's message
            conversation_history: Previous conversation turns

        Returns:
            Agent's response string (questions or final JSON)
        """
        # Build messages list
        messages = conversation_history + [{"role": "user", "content": user_input}]

        # System prompt - defines behavior and output format
        system_prompt = """You are the entry agent for Weave, an AI video generation orchestration system.

Your mission: Understand the user's video concept and gather complete information about characters and storyline.

CONTEXT: Video generation tools like Sora are inconsistent for long-form content (scenes change, characters look different). Weave solves this by maintaining continuity across clips. You're gathering the foundational information needed.

GATHERING PHASE:
Ask clarifying questions to collect:

1. CHARACTERS (for each main character):
   - Name
   - Physical appearance (detailed visual description)
   - Personality traits
   - Role in the story

2. STORYLINE:
   - Overall concept/theme
   - Beginning, middle, end (basic story arc)
   - KEY SCENES (with detailed descriptions):
     * Scene title/label
     * What happens visually in this scene (detailed description for video generation)
     * Which characters appear
     * Setting/location
     * Mood/emotional tone of the scene
   - Overall tone/style (dramatic, comedic, realistic, etc.)

QUESTION ASKING STRATEGY:
- Start by understanding the basic concept
- Ask focused, specific questions (not overwhelming)
- Ask follow-up questions based on answers
- Be conversational and natural
- If user gives vague answers, probe for specifics (especially visual details for characters)

COMPLETION CRITERIA:
Only finalize when you have:
- At least ONE main character with visual description and role
- Clear storyline with beginning/middle/end
- AT LEAST 3 key scenes with detailed descriptions (title, visual description, characters, setting, mood)
- Overall tone/style preference

When gathering scene information, ask about:
- What happens visually in each scene
- Which characters are present
- Where the scene takes place (setting)
- The emotional mood of the scene

When you're confident you have sufficient information, use the finalize_output tool to generate the structured JSON.

DO NOT output JSON directly in your responses - only use the finalize_output tool when ready."""

        # Tool definition - single tool for finalizing output
        tools = [
            {
                "name": "finalize_output",
                "description": "Call this tool when you have gathered sufficient information about characters and storyline. This will generate the final structured JSON output.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "characters": {
                            "type": "array",
                            "description": "List of character objects with their details",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "name": {"type": "string"},
                                    "appearance": {"type": "string", "description": "Detailed visual description"},
                                    "personality": {"type": "string"},
                                    "role": {"type": "string", "description": "Role in the story"}
                                },
                                "required": ["name", "appearance", "role"]
                            }
                        },
                        "storyline": {
                            "type": "object",
                            "description": "Overall storyline information",
                            "properties": {
                                "overview": {"type": "string", "description": "Brief summary of the story"},
                                "scenes": {
                                    "type": "array",
                                    "description": "List of key scenes with detailed descriptions for video generation",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "title": {"type": "string", "description": "Scene title or label"},
                                            "description": {"type": "string", "description": "Detailed visual description of what happens in this scene"},
                                            "characters_involved": {
                                                "type": "array",
                                                "description": "Which characters appear in this scene",
                                                "items": {"type": "string"}
                                            },
                                            "setting": {"type": "string", "description": "Location and environment for this scene"},
                                            "mood": {"type": "string", "description": "Emotional tone of this specific scene"}
                                        },
                                        "required": ["title", "description", "characters_involved", "setting"]
                                    }
                                },
                                "tone": {"type": "string", "description": "Overall tone/style"}
                            },
                            "required": ["overview", "scenes", "tone"]
                        }
                    },
                    "required": ["characters", "storyline"]
                }
            }
        ]

        # Initial API call (FIX: Add await for async client)
        response = await self.client.messages.create(
            model=self.model,
            max_tokens=4096,
            system=system_prompt,
            messages=messages,
            tools=tools
        )

        # Tool use loop (should only happen once when agent is ready to finalize)
        while response.stop_reason == "tool_use":
            # Extract tool uses
            tool_uses = [block for block in response.content if block.type == "tool_use"]

            # Build tool results
            tool_results = []
            for tool_use in tool_uses:
                if tool_use.name == "finalize_output":
                    # Format the JSON output nicely
                    output_data = tool_use.input
                    formatted_json = json.dumps(output_data, indent=2)

                    # Store for next agent
                    self.last_output = output_data

                    return f"""FINAL OUTPUT:

{formatted_json}

✓ Video concept captured!
✓ {len(output_data.get('characters', []))} character(s) outlined
✓ {len(output_data.get('storyline', {}).get('scenes', []))} scene(s) with detailed descriptions

→ Ready for deep character development!
→ Type '/next' to expand characters with the Character Development system
   (6 AI agents will create: psychology, backstory, voice, physical details, story arc, relationships)

→ After that, type '/next' again to reach Scene Creator for final scene refinement
"""

                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": tool_use.id,
                        "content": result_message
                    })
                else:
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": tool_use.id,
                        "content": "Error: Unknown tool"
                    })

            # Continue conversation with tool results
            messages.append({"role": "assistant", "content": response.content})
            messages.append({"role": "user", "content": tool_results})

            # Get next response (FIX: Add await for async client)
            response = await self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                system=system_prompt,
                messages=messages,
                tools=tools
            )

        # Extract final text response
        text_content = [block.text for block in response.content if hasattr(block, "text")]
        return " ".join(text_content)
