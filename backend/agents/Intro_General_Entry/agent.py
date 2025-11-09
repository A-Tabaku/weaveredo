"""
Entry agent for Weave - gathers initial video concept information.
Single LLM system that asks questions and outputs structured JSON when ready.
"""

from typing import List, Dict, Any
import json
from anthropic import Anthropic
from agent_types import AgentLevel
from .tools import TOOLS, execute_tool


class EntryAgent:
    """Entry agent that gathers video concept details through conversation"""

    def __init__(self, api_key: str, level: AgentLevel):
        self.api_key = api_key
        self.level = level
        self.client = Anthropic(api_key=api_key)
        self.model = "claude-sonnet-4-5-20250929"

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

Your mission: Understand the user's general video concept and gather complete information about characters, storyline, AND visual style.

CONTEXT: Video generation tools like Sora are inconsistent for long-form content (scenes change, characters look different). Weave solves this by maintaining continuity across clips. You're gathering the foundational information needed.

GATHERING PHASE (TWO PARTS):

PART 1 - STORY & CHARACTERS:
Ask clarifying questions to collect:

1. CHARACTERS (for each main character):
   - Name
   - Physical appearance (general visual description)
   - Personality traits
   - Role in the story
   - Importance in story (side character, main character, antagonist, etc.)

2. STORYLINE:
   - Beginning, middle, end (basic story arc)
   - Tone (dramatic, comedic, realistic, etc.)

PART 2 - VISUAL STYLE:
After gathering story info, discuss visual style:
- Ask about style preferences (cartoon, realistic, anime, Pixar-style, etc.)
- When user describes a style, use the generate_style_image tool to show them an example
- Present the image path clearly so they can view it
- Ask for feedback on the generated style
- If they want changes, refine the description and generate again
- Iterate until they approve the visual style

QUESTION ASKING STRATEGY:
- Start by understanding the basic concept
- Ask focused, specific questions (not overwhelming)
- Ask follow-up questions based on answers
- Be conversational and natural
- If user gives vague answers, probe for specifics (especially visual details for characters)

USING THE TOOLS:
- generate_style_image: Use when you have a style description to visualize
- finalize_output: ONLY use when you have characters, storyline, AND approved visual style

COMPLETION CRITERIA:
Only finalize when you have:
- At least ONE main character with visual description and role
- Clear storyline with beginning/middle/end
- Tone preference
- APPROVED visual style with generated image

DO NOT output JSON directly in your responses - only use the finalize_output tool when ready."""

        # Use tools from tools.py (includes generate_style_image and finalize_output)
        tools = TOOLS

        # Initial API call
        response = self.client.messages.create(
            model=self.model,
            max_tokens=4096,
            system=system_prompt,
            messages=messages,
            tools=tools
        )

        # Tool use loop - handles both image generation and finalization
        while response.stop_reason == "tool_use":
            print("\n" + "="*60)
            print("🔧 DEBUG: Tool use detected in agent.py")
            print("="*60)

            # Extract tool uses
            tool_uses = [block for block in response.content if block.type == "tool_use"]
            print(f"🔢 Number of tool uses: {len(tool_uses)}")

            # Build tool results
            tool_results = []
            for i, tool_use in enumerate(tool_uses):
                print(f"\n--- Tool Use {i+1} ---")
                print(f"🛠️  Tool Name: {tool_use.name}")
                print(f"🆔 Tool Use ID: {tool_use.id}")
                print(f"📦 Tool Input: {tool_use.input}")

                if tool_use.name == "finalize_output":
                    print("✅ Finalize output triggered - formatting JSON...")
                    # Format the JSON output nicely
                    output_data = tool_use.input
                    formatted_json = json.dumps(output_data, indent=2)
                    return f"FINAL OUTPUT:\n\n{formatted_json}\n\nInformation gathering complete!"

                elif tool_use.name == "generate_style_image":
                    print("🎨 Image generation tool triggered - executing...")
                    # Execute the image generation tool
                    result = await execute_tool(tool_use.name, **tool_use.input)
                    print(f"📤 Tool result: {result}")

                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": tool_use.id,
                        "content": str(result)
                    })

                else:
                    print(f"❌ Unknown tool: {tool_use.name}")
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": tool_use.id,
                        "content": "Error: Unknown tool"
                    })

            # Continue conversation with tool results
            messages.append({"role": "assistant", "content": response.content})
            messages.append({"role": "user", "content": tool_results})

            # Get next response
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                system=system_prompt,
                messages=messages,
                tools=tools
            )

        # Extract final text response
        text_content = [block.text for block in response.content if hasattr(block, "text")]
        return " ".join(text_content)
